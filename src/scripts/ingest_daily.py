
# Status : Created cron job to run every 24 hours. 
# TO-DO : Set up more robust error handling

import requests
import os
from dotenv import load_dotenv
import csv
from pathlib import Path
from datetime import datetime
from datetime import timedelta
import pandas as pd 
from collections import deque

load_dotenv() 

EIA_API_KEY = os.getenv("EIA_API_KEY")
# Path(__file__) will get you the current file path. 
# .parent will go one level higher
BASE_DIR = Path(__file__).parent.parent.parent
FILE_PATH = BASE_DIR/"data/raw/ercot_demand.csv"


with open(FILE_PATH, mode="r", newline="") as f:
    reader = csv.reader(f)
    next(reader, None)
    # deque(d.append(next(reader))) all in one line 
    last_row = deque(reader, maxlen=1)
    previous_time_stamp = last_row[0][0]

format_pattern="%Y-%m-%dT%H"
dt_object = datetime.strptime(previous_time_stamp, format_pattern)
updated_timestamp = dt_object + timedelta(hours=1)
time_stamp = updated_timestamp.strftime(format_pattern)



def fetch_data():
    url = f"https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={EIA_API_KEY}&frequency=hourly&data[0]=value&facets[respondent][]=ERCO&facets[type][]=D&start={time_stamp}&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"

    try:
        request = requests.get(url=url)
        response = request.json()
        return response
    except Exception as e:
        print(e)
        raise RuntimeError(f"Failed API call: {e}") from e
    
data = fetch_data()

filtered_data = data['response']['data']

df = pd.DataFrame(filtered_data)
filtered_df = df[['period','value']]
filtered_df.to_csv(FILE_PATH, mode="a", index=False, header=False)



        


