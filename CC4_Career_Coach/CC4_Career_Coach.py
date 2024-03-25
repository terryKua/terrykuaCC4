import pandas as pd 
import requests 


r = requests.get("https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json")
data = r.json()
#List Restaurants

country_code = pd.read_excel('Country-Code.xlsx')
code = country_code['CountryCode'].unique().tolist()
nation = country_code['Country'].unique().tolist()


table1 = pd.DataFrame()
for i in range(len(data)): 
    restaurants = data[i]['restaurants']
    for j in range(len(restaurants)): 
        restaurant = restaurants[j]['restaurant']
        restaurant_id = restaurant['id']
        restaurantName = restaurant['name']
        location = restaurant['location']
        city = location['city']
        country = location['country_id']
        for k in range(len(country_code)): 
            if country == code[k]:
                country = f"{nation[k]}"
        if country == 17:
            country = "null"

        user_rating = restaurant['user_rating']
        user_rating_votes = user_rating['votes']
        AggregateRating = user_rating['aggregate_rating']
        Cuisines = restaurant['cuisines']
        combine = [{'Restaurant Id': restaurant_id, 'Restaurant Name': restaurantName, 'Country': country, 'City': city, 'User rating votes': user_rating_votes, 'Aggregate rating': AggregateRating, 'Cuisines': Cuisines}]
        table1 = table1.append(combine, ignore_index = True)        
#print(table1)
table1.to_csv('restaurants.csv', index = False)

        
#List restaurant events held in April 2019
# Not all restaurants have events. For example, if event starts from January 2019 to June 2019 then April 2019 is included in the past event. 

table2 = pd.DataFrame()
for i in range(len(data)): 
    restaurants = data[i]['restaurants']
    for j in range(len(restaurants)): 
        restaurant = restaurants[j]['restaurant']
        restaurant_id = restaurant['id']
        restaurantName = restaurant['name']     
        if 'zomato_events' in restaurant:
            zomato_events = restaurant['zomato_events']
            for k in range(len(zomato_events)):
              event = zomato_events[k]['event']
              event_id = event['event_id']
              start_date = event['start_date']
              end_date = event['end_date']
              title = event['title']
              photos = event['photos']
              for l in range(len(photos)):
                photo = photos[l]['photo']
                photoURL = photo['url']
                together = [{'Event Id': event_id,'Restaurant Id': restaurant_id, 'Restaurant Name': restaurantName, 
                             'Photo URL': photoURL, 'Event Title': title, 'Start Date': start_date, 'End Date': end_date}] 
                start_date_dt = pd.to_datetime(start_date)
                end_date_dt = pd.to_datetime(end_date)
                if (start_date_dt > pd.to_datetime('2019-04-30')) and (end_date_dt < pd.to_datetime('2019-04-01')):
                    pass
                else:
                    table2 = table2.append(together, ignore_index = True)                    
        else: 
            continue
#print(table2)        
table2.to_csv('restaurant_events.csv', index = False)

#Determine threshold for different rating text

table3 = pd.DataFrame()
for i in range(len(data)): 
    restaurants = data[i]['restaurants']
    for j in range(len(restaurants)): 
        restaurant = restaurants[j]['restaurant']
        user_rating = restaurant['user_rating']
        Aggregate_Rating = user_rating['aggregate_rating']
        Rating_Text = user_rating['rating_text']
        if Rating_Text == 'Excelente' or Rating_Text == 'Eccellente' or Rating_Text == 'Terbaik' or Rating_Text == 'Skvělé':
            Rating_Text = 'Excellent'
        if Rating_Text == 'Muito Bom' or Rating_Text == 'Velmi dobré' or Rating_Text == 'Bardzo dobrze' or Rating_Text == 'Muy Bueno':
            Rating_Text = 'Very Good' 
        if Rating_Text == 'Skvělá volba' or Rating_Text == 'Bueno': 
            Rating_Text = 'Good' 
        compare = [{'Aggregate rating': Aggregate_Rating, 'RatingText': Rating_Text}]
        if Rating_Text != 'Not rated':
            table3 = table3.append(compare, ignore_index = True)

rating_text = table3['RatingText'].unique().tolist()

query_rating = {}
tableThreshold = pd.DataFrame()
for ratings in rating_text: 
    query_rating = table3.query(f"RatingText == '{ratings}'")
    Min = query_rating['Aggregate rating'].min()
    Max = query_rating['Aggregate rating'].max()
    threshold = [{'Rating Text': f'{ratings}', 'Minimum aggregate': Min, 'Maximum aggregate': Max}]
    tableThreshold = tableThreshold.append(threshold, ignore_index = True)

print(tableThreshold)






