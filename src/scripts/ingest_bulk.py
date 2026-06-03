import requests
import pandas as pd
from dotenv import load_dotenv
import os
from pathlib import Path



load_dotenv()

EIA_API_KEY = os.getenv("EIA_API_KEY")
BASE_DIR = Path(__file__).parent.parent.parent

def fetch_bulk():
    
    offset = 5000; 
    total = 0
    total_response = {}
    
    url = f'https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={EIA_API_KEY}&frequency=hourly&data[0]=value&facets[respondent][]=ERCO&facets[type][]=D&start=2019-01-01T00&sort[0][column]=period&sort[0][direction]=asc&offset=0&length=5000'
    try: 
        request = requests.get(url=url)
        response = request.json()
    except Exception as e:
        print("Error",e)
        raise

    total = int(response['response']['total'])
    total_response = response['response']['data']
    

    while offset < total:
        url = f'https://api.eia.gov/v2/electricity/rto/region-data/data/?api_key={EIA_API_KEY}&frequency=hourly&data[0]=value&facets[respondent][]=ERCO&facets[type][]=D&start=2019-01-01T00&sort[0][column]=period&sort[0][direction]=asc&offset={offset}&length=5000'
        try: 
            request = requests.get(url=url)
            response = request.json()
        except: 
            print("There was an error fetching the data")
        else:
            'The data was read into memory'

        data = response['response']['data']

        total_response += data

        offset+=5000

        print(f"Fetched offset {offset} of {total}")
        
    return total_response


bulk_data = fetch_bulk()

df = pd.DataFrame(bulk_data)
filtered_df = df[['period', 'value']]
filtered_df.to_csv(BASE_DIR/"data/raw/ercot_demand.csv", index=False)

#Test, this is from nano 





