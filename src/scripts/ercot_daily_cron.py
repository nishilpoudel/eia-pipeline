
# Status : API call works 
# To-do : Refactor ingest to sort decreasing, add error handling on both scripts, 
# Create cron job to run every 24 hours. 


import requests
import os
from dotenv import load_dotenv
import csv
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import pandas as pd 

load_dotenv() 

EIA_API_KEY = os.getenv("EIA_API_KEY")
# Path(__file__) will get you the current file path. 
# .parent will go one level higher
BASE_DIR = Path(__file__).parent.parent.parent
FILE_PATH = BASE_DIR/"data/raw/ercot_demand.csv"


with open(FILE_PATH, mode="r", newline="") as f:
    reader = csv.reader(f)
    next(reader, None)
    previous_time_stamp = next(reader, None)[0]


format_pattern="%Y-%m-%dT%H"
dt_object = datetime.strptime(previous_time_stamp, format_pattern)
updated_timestamp = dt_object + timedelta(hours=1)
time_stamp = updated_timestamp.strftime(format_pattern)



def fetch_data():
    url = f"https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={EIA_API_KEY}&frequency=hourly&data[0]=value&facets[respondent][]=ERCO&facets[type][]=D&start={time_stamp}&sort[0][column]=period&sort[0][direction]=desc&offset=0&length=5000"

    try:
        request = requests.get(url=url)
        response = request.json()
        return response
    except Exception as e:
        print(e)
        return
    

data = fetch_data()


filtered_data = data['response']['data']

df = pd.DataFrame(filtered_data)
filtered_df = df[['period','value']]
print(filtered_df)


        


