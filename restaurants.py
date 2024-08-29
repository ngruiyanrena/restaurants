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