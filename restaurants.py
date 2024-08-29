import pandas as pd
from datetime import datetime

# display all columns
pd.set_option('display.max_columns', None)

# Read restaurant_data.json
restaurant_data_url = 'https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json'
restaurant_data_df = pd.read_json(restaurant_data_url)
print(restaurant_data_df)

filtered_df = restaurant_data_df[restaurant_data_df['results_shown'] != 20]
print(len(filtered_df))
print(filtered_df)

# Read country code excel file
country_code_df = pd.read_excel('Country-Code.xlsx')
country_code_df.rename(columns={"Country Code": "country_id", "Country": "country"}, inplace=True)
print(country_code_df)


# Part 1: Extract and store data as restaurants.csv
# restaurant_data_df has 79 rows. 14 of those rows have 0 'results_shown'. Hence, total number of restaurants in csv file should be (79-14)*20 = 1,300.
restaurants_list = []

for index, row in restaurant_data_df.iterrows():
    restaurants = row['restaurants']
    # print(restaurants)
    for restaurant in restaurants:
        restaurant = restaurant['restaurant']
        # print(restaurant)
        restaurants_list.append({
            'restaurant_id': restaurant['id'],
            'restuarant_name': restaurant['name'],
            'country_id': restaurant['location']['country_id'],
            'city': restaurant['location']['city'],
            'user_rating_votes': restaurant['user_rating']['votes'],
            'user_aggregate_rating': restaurant['user_rating']['aggregate_rating'],
            'cuisines': restaurant['cuisines']
        })

restaurants_df = pd.DataFrame(restaurants_list)
print(restaurants_df)

final_restaurants_df = restaurants_df.merge(country_code_df, on='country_id', how='left')
final_restaurants_df.drop(columns=['country_id'], inplace=True)
final_restaurants_df = final_restaurants_df[['restaurant_id', 'restuarant_name', 'country', 'city', 'user_rating_votes', 'user_aggregate_rating', 'cuisines']]
print(final_restaurants_df)

final_restaurants_df.to_csv('restaurants.csv', index=False)


# Part 2: Extract the list of restaurants that have past event in the month of April 2019 and store the data as restaurant_events.csv
# assuming we want the list of all events that happened in the month of April 2019. 
restaurant_events = []

for restaurants in restaurant_data_df['restaurants']:
    # print(restaurants)
    for restaurant in restaurants:
        restaurant = restaurant['restaurant']
        # print(restaurant)
        if "zomato_events" in restaurant.keys():
            events = restaurant['zomato_events']
            # print(events)
            for event in events:
                event = event['event']
                # print(event)
                start_date = datetime.strptime(event['start_date'], '%Y-%m-%d')
                end_date = datetime.strptime(event['end_date'], '%Y-%m-%d')
                if start_date.strftime('%Y-%m') <= '2019-04' and end_date.strftime('%Y-%m') >= '2019-04':
                    # print(event)
                    restaurant_events.append({
                        'event_id': event['event_id'],
                        'restaurant_id': restaurant['id'],
                        'restaurant_name': restaurant['name'],
                        'photo_url': event['photos'][0]['photo']['url'] if len(event['photos']) != 0 else 'N/A', # assuming we want the first photo url for each event 
                        'event_title': event['title'],
                        'event_start_date': event['start_date'],
                        'event_end_date': event['end_date']
                    })
                else :
                    print(f"did not happen in april 2019: {event}")

restaurant_events_df = pd.DataFrame(restaurant_events)
print(restaurant_events_df)

restaurant_events_df.to_csv('restaurant_events.csv', index=False)


# Part 3: From the dataset (restaurant_data.json), determine the threshold for the different rating text based on aggregate rating. 
ratings_list = []

for restaurants in restaurant_data_df['restaurants']:
    # print(restaurants)
    for restaurant in restaurants:
        restaurant = restaurant['restaurant']
        # print(restaurant)
        ratings_list.append({
            'aggregate_rating': restaurant['user_rating']['aggregate_rating'],
            'rating_text': restaurant['user_rating']['rating_text']
        })

ratings_df = pd.DataFrame(ratings_list)
print(ratings_df)

ratings_df = ratings_df[ratings_df['rating_text'].str.contains('Excellent|Very Good|Good|Average|Poor')]
threshold = ratings_df.groupby('rating_text').agg({'aggregate_rating': ['min', 'max']})
print(threshold)