import requests
import pandas as pd
import os
import numpy as np
import json
import networkx as nx
from math import radians, cos, sin, asin, sqrt
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
    

class Vehicle_Network:
    '''Fuel Types: ELEC - Electric vehicle, LPG - Propane vehicle, BD - Biodiesel, CNG - compresses natural gas 
    this creates a comlete graph, meaning that all vehicle routes are possible. This network will be pruned when the 
    user enters in a range for their vehicle. I think this may be faster, especially if each Vehicle_Network is saved and imported
    when needed
    
    '''
    
    def __init__(self,refill_locations,vehicle_fuel):
        self.vehicle_fuel = vehicle_fuel #user must select one fuel type.
        self.refill_locations = refill_locations #the data from the NREL API
        #self.refill_locations = self.refill_locations[self.refill_locations['fuel_type_code']==self.vehicle_fuel]
        self.G = nx.Graph() 
        #add more variables to filter data if needed
    
        #from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        """
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles, 6371 for km
        return (c * r)

    def create_graph(self):
        
        #TODO: filter data and check for errors at this point
        #add the graph nodes
        for index,row in self.refill_locations.iterrows():
            
            #TODO: add more descriptors (columns) to the graph if neccecary
            self.G.add_node(str(row['city'])+'_'+str(row['zip']),
                       city=row['city'],
                       country=row['country'],
                       ev_pricing=row['ev_pricing'],
                       facility_type=row['facility_type'],
                       fuel = row['fuel_type_code'],
                       lat = row['latitude'],
                       long = row['longitude'],
                       province = row['state'],
                       station_name = row['station_name'],
                       address = row['street_address'])
        
        #add the graph edges
        #This probably runs in n^2 time. Maybe look for a better wau to add edges, only when certain conditions are met...
        for node1 in self.G:
            for node2 in self.G:
                if node1 != node2 and not self.G.has_edge(node1,node2):
                    
                    lat1,long1 = self.G.node[node1]['lat'],self.G.node[node1]['long']
                    lat2,long2 = self.G.node[node2]['lat'],self.G.node[node2]['long']
                    distance = self.haversine(long1,lat1,long2,lat2)
                    #there is no range requirement
                    self.G.add_edge(node1,node2,weight=distance)
                        
        #TODO: once the graphs are created, they should be pickled, and then pruned later. This will make it much faster
        return(self.G)

class Vehicle_Route:
    
    def __init__(self,G,vehicle_range):
        self.vehicle_range = vehicle_range #user must select one fuel type.
        self.G = G #this is the fully connected graph. Need to 'prune it'
    
    def prune(self):
        None
        
        for nodes in G:
            
            for neighbors in G[nodes]:
                
                if neighbors['weight'] > self.vehicle_range:
                    #remove the edge!
                else:
                    #keep the edge
    

#%%
#TODO: graph the network...
if __name__ == "__main__":
    df = get_stations()
    path = Vehicle_Network(refill_locations=df,vehicle_fuel = 'ELEC')
    route  = path.create_graph()
    
    
#%%