import requests
import pandas as pd
import os
import numpy as np
import json
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#%%

def config_file(config_file):
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname('__file__')))
        
    try:
        with open(os.path.join(__location__,config_file)) as f:
            config = json.load(f)
            return(config)

    except:
        raise

def api_url(key,url='https://developer.nrel.gov/api/alt-fuel-stations/v1.json?country=CA&api_key=YOUR_KEY_HERE'):
    url = url.replace('YOUR_KEY_HERE',key)
    return(url)

def request_api(url):
    r = requests.get(url,allow_redirects=True, stream=True, headers=headers).json() #returns a dictionary
    df = pd.DataFrame(r['fuel_stations'])
    return(df)

def get_stations(file_name='fuel_stations.csv'):
    if os.path.isfile(file_name):
        df = pd.read_csv(file_name)
        print('read file from: '+os.getcwd())
    else:
        key = config_file('api_key.json')['key']
        url = api_url(key)
        df = request_api(url)
        df.to_csv(file_name,index=False)
        print('api request: '+str(url))
    
    return(df)
    


#%%
#main
df = get_stations()
