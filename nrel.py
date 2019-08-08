import requests
import pandas as pd
import os
import numpy as np
import json
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import pickle
import matplotlib.pylab as plt
from pandas.plotting import register_matplotlib_converters
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#%%
#TODO: make all data functions into a class with the ability to set new data.
#Vehicle_Network can inherit data and create a new complete graph if neccecary

class Data:
    
    def __init__(self,new_data=False,nrel_data='fuel_stations.csv'):
        self.new_data = new_data
        self.nrel_data = nrel_data

    @staticmethod
    def config_file(config_file):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname('__file__')))
            
        try:
            with open(os.path.join(__location__,config_file)) as f:
                config = json.load(f)
                return(config)
    
        except:
            raise
            
    @staticmethod
    def api_url(key,url='https://developer.nrel.gov/api/alt-fuel-stations/v1.json?country=CA&api_key=YOUR_KEY_HERE'):
        url = url.replace('YOUR_KEY_HERE',key)
        return(url)
    
    @staticmethod
    def request_api(url):
        r = requests.get(url,allow_redirects=True, stream=True, headers=headers).json() #returns a dictionary
        df = pd.DataFrame(r['fuel_stations'])
        return(df)
    
    def get_stations(self):
        if os.path.isfile(self.nrel_data):
            df = pd.read_csv(self.nrel_data)
            print('read file from: '+os.getcwd())
        else:
            key = Data.config_file('api_key.json')['key']
            url = Data.api_url(key)
            df = Data.request_api(url)
            df.to_csv(self.nrel_data,index=False)
            print('api request: '+str(url))
        
        return(df)
    
    @staticmethod
    def delete_file(name):
        if os.path.isfile(name):
            os.remove(name)
            
    
    def station_data(self):
        if self.new_data==True:
            Data.delete_file(self.nrel_data)
            #also delete all of the graph pickles!!
        df = self.get_stations()
        #create all the graphs!
        return(df)
            
            
    
class VehicleNetwork(Data):
    
    '''
    Fuel Types: ELEC - Electric vehicle, LPG - Propane vehicle, BD - Biodiesel, CNG - compresses natural gas 
    this creates a comlete graph, meaning that all vehicle routes are possible. This network will be pruned when the 
    user enters in a range for their vehicle. I think this may be faster, especially if each Vehicle_Network is saved and imported
    when needed
    '''
    
    #limits the amount of stations for testing purposes.
    sample_stations = 500
    sample_province = 'AB'
    
    def __init__(self,vehicle_fuel,vehicle_range,limit,new_data=False):
        Data.__init__(self,new_data=new_data)
        self.vehicle_fuel = vehicle_fuel #user must select one fuel type.
        self.refill_locations = self.station_data() #from nrel api
        self.limit = limit
        self.vehicle_range = vehicle_range
        #self.refill_locations = self.refill_locations[self.refill_locations['fuel_type_code']==self.vehicle_fuel]
        #self.G = nx.Graph() 
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
        
        if self.limit == True:
            self.refill_locations = self.refill_locations[self.refill_locations['state']==VehicleNetwork.sample_province]
            #self.refill_locations = self.refill_locations.sample(n=Vehicle_Network.sample_stations)
            

        file_name = self.vehicle_fuel+'.pickle'
        
        if os.path.isfile(file_name):
            G = nx.read_gpickle(file_name)
            print('read pickle object: '+file_name)
        else:
            G = nx.Graph()
            for index,row in self.refill_locations.iterrows():
                
                #TODO: add more descriptors (columns) to the graph if neccecary
                G.add_node(str(row['city'])+'_'+str(row['zip']),
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
            for node1 in G:
                for node2 in G:
                    if node1 != node2 and not G.has_edge(node1,node2):
                        
                        lat1,long1 = G.node[node1]['lat'],G.node[node1]['long']
                        lat2,long2 = G.node[node2]['lat'],G.node[node2]['long']
                        distance = self.haversine(long1,lat1,long2,lat2)
                        #there is no range requirement
                        G.add_edge(node1,node2,weight=distance)
                            
            #pickle the graph once it is created
            nx.write_gpickle(G,file_name)
            print('created new pickle object: '+file_name)
            
        return(G)
    
    def vehicle_route(self):
        
        G = self.create_graph()
        #nx.draw(G)
        
        remove_list = []
        for paths in G.edges(data=True):
            
            n1 = paths[0]
            n2 = paths[1]
            distance = paths[2]['weight']

            if distance > self.vehicle_range:
                remove_list.append(tuple((n1,n2)))
        
        G.remove_edges_from(remove_list)

        #nx.draw(G)
        return(G)
    
    def shortest_path(self,start,end):
        
        G  = self.vehicle_route()
    
        def get_random_location(loc):
            locations = self.refill_locations[self.refill_locations['city']==loc].copy()
            location = locations.sample(n=1) #should be one row of a dataframe
            n = location.iloc[0]['city']+'_'+location.iloc[0]['zip']
            return(n)
        
        source,target = get_random_location(start),get_random_location(end)
        #TODO: an error gets raised if there is no viable route..
        path = nx.shortest_path(G,source=source,target=target)
        #add the "gas station" algorithm to see if any of the nodes (stations) can be passed over. This shouldnt be the case
    
        return(path)
    

#%%
if __name__ == "__main__":
    #TODO: sensitivity test to determine the min range needed to go across Canada
    path = VehicleNetwork(vehicle_fuel = 'ELEC',vehicle_range=200,limit=False)
    route = path.shortest_path(start='Vancouver',end='Halifax')
    

#%%
