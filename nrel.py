import requests
import pandas as pd
import os
import numpy as np
import json
import networkx as nx
from math import radians, cos, sin, asin, sqrt
import pickle
#import matplotlib.pylab as plt
from pandas.plotting import register_matplotlib_converters
import warnings
import re
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#%%

class Data:
    '''
    NREL API documentation: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/
    '''
    
    max_range = 500
    min_range = 50
    sample_stations = 500
    country_options = ['CA','US']
    sample_province = 'AB'
    
    def __init__(self,vehicle_fuel,region,limit,new_data=False,nrel_data='fuel_stations.csv'):
        self.vehicle_fuel = vehicle_fuel
        self.region = region
        self.new_data = new_data
        self.nrel_data = nrel_data
        self.limit = limit
    
    
    def FileName(self):
        return(self.vehicle_fuel+'_'+self.region+'_'+'Max_'+str(Data.max_range)+'_'+'Min_'+str(Data.min_range)+'.pickle')
        
    def __str__(self):
        return('')

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
    def api_url(key,country,url='https://developer.nrel.gov/api/alt-fuel-stations/v1.json?country=CO&api_key=YOUR_KEY_HERE'):
        url = url.replace('YOUR_KEY_HERE',key)
        url = url.replace('CO',country)
        return(url)
    
    @staticmethod
    def request_api(url):
        r = requests.get(url,allow_redirects=True, stream=True, headers=headers).json() #returns a dictionary
        df = pd.DataFrame(r['fuel_stations'])
        return(df)
    
    def get_stations(self):
        if os.path.isfile(self.nrel_data):
            stations = pd.read_csv(self.nrel_data,dtype={'access_code': 'object', 
                                                         'access_days_time': 'object', 
                                                         'access_detail_code': 'object', 
                                                         'cards_accepted': 'object', 
                                                         'date_last_confirmed': 'object', 
                                                         'expected_date': 'object', 
                                                         'fuel_type_code': 'object', 
                                                         'groups_with_access_code': 'object', 
                                                         'id': 'int64', 
                                                         'open_date': 'object', 
                                                         'owner_type_code': 'object', 
                                                         'status_code': 'object', 
                                                         'station_name': 'object', 
                                                         'station_phone': 'object', 
                                                         'updated_at': 'object', 
                                                         'facility_type': 'object', 
                                                         'geocode_status': 'object', 
                                                         'latitude': 'float64', 
                                                         'longitude': 'float64', 
                                                         'city': 'object', 
                                                         'intersection_directions': 'object', 
                                                         'plus4': 'float64', 
                                                         'state': 'object', 
                                                         'street_address': 'object', 
                                                         'zip': 'object', 
                                                         'country': 'object', 
                                                         'bd_blends': 'object', 
                                                         'cng_dispenser_num': 'float64', 
                                                         'cng_fill_type_code': 'object', 
                                                         'cng_psi': 'object', 
                                                         'cng_renewable_source': 'object', 
                                                         'cng_total_compression': 'float64', 
                                                         'cng_total_storage': 'float64', 
                                                         'cng_vehicle_class': 'object', 
                                                         'e85_blender_pump': 'object', 
                                                         'e85_other_ethanol_blends': 'object', 
                                                         'ev_connector_types': 'object', 
                                                         'ev_dc_fast_num': 'float64', 
                                                         'ev_level1_evse_num': 'float64', 
                                                         'ev_level2_evse_num': 'float64', 
                                                         'ev_network': 'object', 
                                                         'ev_network_web': 'object', 
                                                         'ev_other_evse': 'object', 
                                                         'ev_pricing': 'object', 
                                                         'ev_renewable_source': 'object', 
                                                         'hy_is_retail': 'object', 
                                                         'hy_pressures': 'object', 
                                                         'hy_standards': 'object', 
                                                         'hy_status_link': 'object', 
                                                         'lng_renewable_source': 'float64', 
                                                         'lng_vehicle_class': 'object', 
                                                         'lpg_primary': 'object', 
                                                         'lpg_nozzle_types': 'object', 
                                                         'ng_fill_type_code': 'object', 
                                                         'ng_psi': 'object', 
                                                         'ng_vehicle_class': 'object', 
                                                         'access_days_time_fr': 'object', 
                                                         'intersection_directions_fr': 'object', 
                                                         'bd_blends_fr': 'float64', 
                                                         'groups_with_access_code_fr': 'object', 
                                                         'ev_pricing_fr': 'object', 
                                                         'ev_network_ids': 'object', 
                                                         'federal_agency': 'object'})
            #print('read file from: '+os.getcwd())
        else:
            key = Data.config_file('api_key.json')['key']
            #get both countries
            country_frames = []
            
            for country in self.country_options:
                url = Data.api_url(key,country)
                df = Data.request_api(url)
                country_frames.append(df)
                print('api request: '+str(url))
            
            stations = pd.concat(country_frames,axis=0,sort=False,ignore_index=True)
            stations.to_csv(self.nrel_data,index=False)
        
        return(stations)
    
    @staticmethod
    def delete_file(name):
        if os.path.isfile(name):
            os.remove(name)
            
    
    def station_data(self):
        if self.new_data==True:
            Data.delete_file(self.nrel_data)
            #also delete all of the graph pickles!!
        df = self.get_stations()
        #limit the data to the appropriate fuel type
        df = df[df['fuel_type_code']==self.vehicle_fuel]
        #get the chosen region
        if self.region != 'NA':
            df = df[df['country']==self.region]
        
        return(df)
    
    #from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def haversine(self,lon1, lat1, lon2, lat2):
        """
        Calculate the great circle distance between two points 
        on the earth (specified in decimal degrees)
        This is set to km for default
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
        '''
        creates a semi-complete graph if there isnt already one available in binary form. The graph connectivity is limited by the maximum range.
        A higher max range allows you to view hypothetical vehicle routes that are not available with current EV technology, but it makes the 
        optimal path calculation much slower.
        '''
        #TODO: look at casting types for node attributes and edge weight. This may reduce pickle file size
        #TODO: remove limit instance variable after testing is complete!
        #if self.limit == True:
        #    self.refill_locations = self.refill_locations[self.refill_locations['state']==VehicleNetwork.sample_province]
            #self.refill_locations = self.refill_locations.sample(n=Vehicle_Network.sample_stations)
            

        #file_name = self.vehicle_fuel+'.pickle'
        file_name = self.FileName()
        refill_locations = self.station_data()        
        
        if os.path.isfile(file_name):
            G = nx.read_gpickle(file_name)
            print('read pickle object: '+file_name)
        else:
            #ceates a complete graph if there isnt one already
            print('creating pickle object: '+file_name)
            print(len(refill_locations))
            G = nx.Graph()
            for index,row in refill_locations.iterrows():
                
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
            #This probably runs in n^2 time. Maybe look for a better way to add edges, only when certain conditions are met...
            #look at using a hash table that stores the distance between two nodes. This is a O(1) lookup...
            #TODO: come up with all unique pairs in node list, and then add edges... (https://stackoverflow.com/questions/18201690/get-unique-combinations-of-elements-from-a-python-list)
            for node1 in G:
                for node2 in G:
                    if node1 != node2 and not G.has_edge(node1,node2):
                        
                        lat1,long1 = G.node[node1]['lat'],G.node[node1]['long']
                        lat2,long2 = G.node[node2]['lat'],G.node[node2]['long']
                        distance = self.haversine(long1,lat1,long2,lat2)
                        #there is no range requirement
                        
                        if distance > Data.max_range or distance < Data.min_range:
                            None #the vehicle cant conceivably make it from node 1 to node 2
                        else:    
                            G.add_edge(node1,node2,weight=distance)
                            
            #pickle the graph once it is created
            nx.write_gpickle(G,file_name)
            print('created new pickle object: '+file_name+' with max range '+str(self.max_range))
            
        return(G)
    
    @staticmethod
    def create_pickes(max_range=None,min_range=None): #TODO: make this work...
        '''
        convenience method for creating all pickles at once
        '''
        Data.max_range = max_range
        Data.min_range = min_range
        
        fuel_options = ['ELEC','LPG','CNG'] #TODO: add fuel_options to self
        Data.country_options.append('NA')
    
        for fuel in fuel_options:
            for country in Data.country_options:
                #self.create_graph()
                network = Data(vehicle_fuel=fuel,region=country,limit=None)
                network.create_graph()
    
            
#TODO: make the graph (G) an intance variable. This will make it easier to modify the graph range in a VehicleNetwork method
class VehicleNetwork(Data):
    #TODO: NA doesnt work as a region...
    '''
    Fuel Types: ELEC - Electric vehicle, LPG - Propane vehicle, BD - Biodiesel, CNG - compresses natural gas 
    this creates a comlete graph, meaning that all vehicle routes are possible. This network will be pruned when the 
    user enters in a range for their vehicle. I think this may be faster, especially if each Vehicle_Network is saved and imported
    when needed
    '''
    
    
    def __init__(self,vehicle_fuel,region='CA',vehicle_range=0,new_data=False):
        Data.__init__(self,vehicle_fuel,region,limit=False,new_data=new_data)
        self.vehicle_fuel = vehicle_fuel #user must select one fuel type.
        self.refill_locations = self.station_data() #from nrel api
        self.vehicle_range = vehicle_range #user sets the range for their vehicle
        self.G = self.create_graph() #read in the graph
        self.refill_locations = self.station_data() #read in the df. Make sure that refill_locations is used throughout this class!
        #add more variables to filter data if needed
    
    #getter
    def get_G(self):
        return(self.G)
    
    def get_df(self):
        return(self.refill_locations)
    
    def available_cities(self):
        cities = list(self.refill_locations['city'])
        return(cities)
    
    def source_destination(self):
        #TODO: move the source/destination checking to the first step! This will make it faster...
        return(None)
    
    #setter
    def vehicle_route(self):
        
        remove_list = []
        for paths in self.G.edges(data=True):
            
            n1 = paths[0]
            n2 = paths[1]
            distance = paths[2]['weight']

            if distance > self.vehicle_range:
                remove_list.append(tuple((n1,n2)))
        
        self.G.remove_edges_from(remove_list)
        #return(self.G)
            
    
    def shortest_path(self,start,end):
        
        #use getters and setters for this!
        #self.vehicle_route()
        #TODO: make get_random_location into a verify_data method
        def get_random_location(loc,city_type):
            #first check to see if the loc is in the city list
            if loc in self.available_cities():
            
                locations = self.refill_locations[self.refill_locations['city']==loc].copy()
                #raise a warning if the size of locations == 0. This means there isnt a station in that city
                if len(locations) == 0:
                    warnings.simplefilter('error')
                    warnings.warn('There are no '+self.vehicle_fuel+' stations '+'in '+loc)
                    
                location = locations.sample(n=1) #should be one row of a dataframe
                n = str(location.iloc[0]['city'])+'_'+str(location.iloc[0]['zip'])
            else:
                warnings.simplefilter('error')
                warnings.warn(loc+' is not a valid city. Did you mean:')
                
            return(n) #TODO: add return that checks if user input is valid!
        
        source,target = get_random_location(start,city_type='start location'),get_random_location(end,city_type='end location')
        self.vehicle_route()
        #TODO: an error gets raised if there is no viable route.. Implement an optimizer that returns the vehicle range that makes the route possible!
        #TODO: make sure that self.G has been properly filtered!
        path_data = {}
        path_data['fuel'] = self.vehicle_fuel
        path_data['region'] = self.region
        path_data['user input start'] = start
        path_data['user input end'] = end
        path_data['vehicle range'] = self.vehicle_range
        
        try:
            path = nx.shortest_path(self.G,source=source,target=target)
            path_data['route'] = path
            path_data['number of stops'] = len(path)
            #the path variable is a list of nodes. Now access node attributes to get lat/long,etc
            path_data_detail = []
            cumulative_distance,weight = 0,0
            for stop_number,stop in enumerate(path):
                
                if stop_number == 0:
                    None
                elif stop_number < len(path):
                    weight = self.G[path[stop_number-1]][path[stop_number]]['weight']
                    cumulative_distance = cumulative_distance+weight
                else:
                    None
                
                
                attributes = self.G.node[stop]
                path_data_detail.append({stop:{'latitude':attributes['lat'],
                                               'longitude':attributes['long'],
                                               'fuel':attributes['fuel'],
                                               'city':attributes['city'],
                                               'ev_pricing':attributes['ev_pricing'],
                                               'facility_type':attributes['facility_type'],
                                               'address':attributes['address'],
                                               'province':attributes['province'],
                                               'station_name':attributes['station_name'],
                                               'cumulative_distance':cumulative_distance,
                                               'distance from previous node':weight}})
            
            path_data['total distance'] = cumulative_distance    
            path_data['detailed path'] = path_data_detail
            #if a path can be found:
            path_data['route found'] = True
        except:
            path_data['route found'] = False
            path_data['detailed path'] = None
            path_data['total distance'] = None
            raise
            #TODO: raise a warning that the route didnt work, and then inform the user that a new path is being calculated with a higher range!
        
        
        #add the "gas station" algorithm to see if any of the nodes (stations) can be passed over. This shouldnt be the case
        #Algorithm example: https://www.coursera.org/lecture/algorithmic-toolbox/car-fueling-8nQK8
        #just because a car goes through a node, does not neccecarily mean that it needs to fuel!
        
        return(path_data) #TODO: round everything...
    
        
#%%
if __name__ == "__main__":
    #Data.create_pickes(max_range=500,min_range=50)
    path = VehicleNetwork(vehicle_fuel = 'ELEC',vehicle_range=250,region='NA')
    #G = path.get_G()
    route = path.shortest_path(start='Edmonton',end='London')
    #cities = path.available_cities()
    #df = path.get_stations()
    
#%%
route = path.shortest_path(start='Edmonton',end='London')