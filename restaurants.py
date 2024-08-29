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