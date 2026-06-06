
# Status : Created cron job to run every 24 hours. 
# TO-DO : Set up more robust error handling

import requests
import os
from dotenv import load_dotenv
import csv
from pathlib import Path
from datetime import datetime, timedelta, timezone
import pandas as pd 
from collections import deque
import sys

load_dotenv() 

EIA_API_KEY = os.getenv("EIA_API_KEY")
# Path(__file__) will get you the current file path. 
# .parent will go one level higher
BASE_DIR = Path(__file__).parent.parent.parent
FILE_PATH = BASE_DIR/"data/raw/ercot_demand.csv"
FORMAT_PATTERN = "%Y-%m-%dT%H"


#Read latest timestamp from csv and return next timestamp to fetch
def get_next_timestamp(file_path):

    with open(file_path, mode="r", newline="") as f:
        reader = csv.reader(f)
        next(reader, None)
        # deque(d.append(next(reader))) all in one line 
        last_row = deque(reader, maxlen=1)
        latest_time_stamp = last_row[0][0]

    dt_object = datetime.strptime(latest_time_stamp, FORMAT_PATTERN)
    next_timestamp = dt_object + timedelta(hours=1)
    return next_timestamp.strftime(FORMAT_PATTERN)

    
#Fetch ercot demand data
def fetch_data(time_stamp):
    url = f"https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={EIA_API_KEY}&frequency=hourly&data[0]=value&facets[respondent][]=ERCO&facets[type][]=D&start={time_stamp}&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000"

    try:
        response = requests.get(url=url)
        return response.json()
    except Exception as e:
        print(e)
        raise RuntimeError(f"Failed API call: {e}") from e
    

#Filter for time and demand(value) and append to csv
def process_and_save(data, file_path):
    
    filtered_data = data['response']['data']

    if not filtered_data:
        print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] No new data available. Exiting!")
        sys.exit(0)
    
    df = pd.DataFrame(filtered_data)
    filtered_df = df[['period','value']]
    filtered_df.to_csv(file_path,mode='a',index=False, header=False)
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}] Appended {len(filtered_df)} rows!" )

def main():
    time_stamp = get_next_timestamp(FILE_PATH)
    data = fetch_data(time_stamp)
    process_and_save(data, FILE_PATH)
    

if __name__ == "__main__":
    main()
