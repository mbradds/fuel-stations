import requests
import pandas as pd
import os
import json
import networkx as nx
import random
from math import radians, cos, sin, asin, sqrt
from itertools import combinations
import warnings
import pickle
from networkY import Graph
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#%%

class Location:
    
    #TODO: move the api/data methods here
    def __init__(self,vehicle_fuel,start,end,nrel_data='fuel_stations.csv'):
        self.vehicle_fuel = vehicle_fuel
        self.nrel_data = nrel_data
        self.start = start
        self.end = end
    
    def get_stations(self):
        #print('called get_stations')
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
        
        stations = stations[stations['fuel_type_code']==self.vehicle_fuel]
        return(stations)   
        
    
    def find_region(self,custom=None):
        
        df = self.get_stations()
        
        def get_random_location(loc,df):
            
            df = df[df['city']==loc].copy()
            unique = [str(c).capitalize()+'_'+str(p) for c,p in zip(df['city'],df['zip'])]
            unique = list(set(unique))
            
            #raise a warning if the size of locations == 0. This means there isnt a station in that city
            if len(unique) == 0:
                warnings.simplefilter('error')
                warnings.warn('There are no '+self.vehicle_fuel+' stations '+'in '+loc)
                    
            #location = locations.sample(n=1) #should be one row of a dataframe
            n = random.choice(unique)

            return(n) 
        
        
        def split_location(loc):
            loc = loc.lower()
            l = loc.split(',')
            if len(l) < 2:
                l.append(None)
            
            c = df.copy()
            c['city'] = [str(x).lower() for x in c['city']]
            c['state'] = [str(x).lower() for x in c['state']]
            
            try:

                if l[1] == None:
                    location = c[c['city']==l[0]]
                else:
                    location = c[(c['city']==l[0]) & (c['state']==l[1])]
            except:
                #raise an error. No stations could be found
                location = None
            
            #get a random station ("node")
            
            node = get_random_location(l[0],location)
            
            station_count = {}
            max_stations = 0
            for r in list(location['country'].unique()):
                number_of_stations = len(location[location['country']==r])
                if number_of_stations > max_stations:
                    max_stations = number_of_stations
                    
                station_count[number_of_stations] = r
            
            return(station_count[max_stations],node)
        
        
        start_country,start_node = split_location(self.start)
        end_country,end_node = split_location(self.end)
        
        if custom == None:
            if start_country == end_country:
                r = start_country
                #return(start_country,start_node,end_node)
            else:
                r = 'NA'
                #return('NA',start_node,end_node)
        else:
            r = custom

        if r != 'NA':
            df = df[df['country']==r].copy()
        
        return(r,start_node,end_node,df) 
    
class Data(Location):
    
    #TODO: use setter on region depending on start and end values.
    '''
    NREL API documentation: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/
    '''
    max_range = 500
    min_range = 50
    country_options = ['CA','US']
    
    def __init__(self,vehicle_fuel,start,end,graph_type,nrel_data='fuel_stations.csv',custom=None):
        Location.__init__(self,vehicle_fuel,start,end)
        self.graph_type = graph_type
        self.vehicle_fuel = vehicle_fuel
        self.nrel_data = nrel_data
        self.start = start
        self.end = end
        self.region,self.start_node,self.end_node,self.stations = Location.find_region(self,custom)
     
    
    def FileName(self):
        return(self.graph_type+'/'+self.vehicle_fuel+'_'+self.region+'_'+'Max_'+str(Data.max_range)+'_'+'Min_'+str(Data.min_range)+'.pickle')
        

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
        
    
    @staticmethod
    def delete_file(name):
        if os.path.isfile(name):
            os.remove(name)
            
                    
    
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
    
    def create_graph_ny(self):
        print('called create_graph_ny')
        '''
        creates a semi-complete graph if there isnt already one available in binary form. The graph connectivity is limited by the maximum range.
        A higher max range allows you to view hypothetical vehicle routes that are not available with current EV technology, but it makes the 
        optimal path calculation much slower.
        '''
        #TODO: look at casting types for node attributes and edge weight. This may reduce pickle file size
        #TODO: remove limit instance variable after testing is complete!            

        file_name = self.FileName()
                
        if os.path.isfile(file_name):
            infile = open(file_name,'rb')
            G = pickle.load(infile)
            infile.close()
            print('read pickle object: '+file_name)
        else:
            #ceates a complete graph if there isnt one already
            print('creating pickle object: '+file_name)
            print('DF length: '+str(len(self.stations)))
            G = Graph()
            for index,row in self.stations.iterrows():
                
                #TODO: add more descriptors (columns) to the graph if neccecary
                G.addNode(node=str(row['city'])+'_'+str(row['zip']),
                           attributes={'city':row['city'],
                                       'country':row['country'],
                                       'ev_pricing':row['ev_pricing'],
                                       'facility_type':row['facility_type'],
                                       'fuel':row['fuel_type_code'],
                                       'lat':row['latitude'],
                                       'long':row['longitude'],
                                       'province':row['state'],
                                       'station_name':row['station_name'],
                                       'address':row['street_address']})
            
            #add the graph edges
            print('Nodes: '+str(G.number_of_nodes()))
            edges = list(combinations(G.nodes(),2))
            print('Edges: '+str(G.number_of_edges()))
            
            for edge in edges:
                lat1,long1 = G.node(edge[0])['attributes']['lat'],G.node(edge[0])['attributes']['long']
                lat2,long2 = G.node(edge[1])['attributes']['lat'],G.node(edge[1])['attributes']['long']
                distance = self.haversine(long1,lat1,long2,lat2)
                #there is no range requirement
                        
                if distance > Data.max_range or distance < Data.min_range:
                    None #the vehicle cant make it from node 1 to node 2
                else:    
                    G.addEdge(edge[0],edge[1],weight=distance)
                                            
            #pickle the graph once it is created
            outfile = open(file_name,'wb')
            pickle.dump(G.getGraph(),outfile)
            outfile.close()
            print('created new pickle object: '+file_name+' with max range '+str(self.max_range))
            
        return(G)
    
    
    def create_graph(self):
        print('called create_graph')
        '''
        creates a semi-complete graph if there isnt already one available in binary form. The graph connectivity is limited by the maximum range.
        A higher max range allows you to view hypothetical vehicle routes that are not available with current EV technology, but it makes the 
        optimal path calculation much slower.
        '''
        #TODO: look at casting types for node attributes and edge weight. This may reduce pickle file size
        #TODO: remove limit instance variable after testing is complete!            

        file_name = self.FileName()
                
        if os.path.isfile(file_name):
            G = nx.read_gpickle(file_name)
            print('read pickle object: '+file_name)
        else:
            #ceates a complete graph if there isnt one already
            print('creating pickle object: '+file_name)
            print('DF length: '+str(len(self.stations)))
            G = nx.Graph()
            for index,row in self.stations.iterrows():
                
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
            print('Nodes: '+str(len(G.nodes)))
            edges = list(combinations(list(G.nodes),2))
            print('Edges: '+str(len(edges)))
            
            for edge in edges:
                lat1,long1 = G.node[edge[0]]['lat'],G.node[edge[0]]['long']
                lat2,long2 = G.node[edge[1]]['lat'],G.node[edge[1]]['long']
                distance = self.haversine(long1,lat1,long2,lat2)
                #there is no range requirement
                        
                if distance > Data.max_range or distance < Data.min_range:
                    None #the vehicle cant make it from node 1 to node 2
                else:    
                    G.add_edge(edge[0],edge[1],weight=distance)
                                            
            #pickle the graph once it is created
            nx.write_gpickle(G,file_name)
            print('created new pickle object: '+file_name+' with max range '+str(self.max_range))
            
        return(G)
        
    
    @staticmethod
    def create_pickes(max_range=None,min_range=None,graph_type='nx_pickles'): #TODO: make this work...
        '''
        convenience method for creating all pickles at once
        '''
        Data.max_range = max_range
        Data.min_range = min_range
        
        fuel_options = ['ELEC','LPG','CNG'] #TODO: add fuel_options to self
        Data.country_options.append('NA')
    
        for fuel in fuel_options:
            for country in Data.country_options:
                
                network = Data(start='Calgary',end = 'Edmonton',vehicle_fuel=fuel,custom=country,graph_type=graph_type)
                if graph_type == 'nx_pickles':
                    network.create_graph()
                elif graph_type == 'ny_pickles':
                    network.create_graph_ny()
                else:
                    print('Pick nx_pickles or ny_pickles')
    
            
#TODO: make the graph (G) an intance variable. This will make it easier to modify the graph range in a VehicleNetwork method
class VehicleNetwork(Data):
    #TODO: NA doesnt work as a region...
    '''
    Fuel Types: ELEC - Electric vehicle, LPG - Propane vehicle, BD - Biodiesel, CNG - compresses natural gas 
    this creates a comlete graph, meaning that all vehicle routes are possible. This network will be pruned when the 
    user enters in a range for their vehicle. I think this may be faster, especially if each Vehicle_Network is saved and imported
    when needed
    '''
    
    def __init__(self,vehicle_fuel,start,end,vehicle_range,graph_type='nx_pickles'):
        Data.__init__(self,vehicle_fuel,start,end,graph_type)
        self.vehicle_fuel = vehicle_fuel #user must select one fuel type.
        self.vehicle_range = vehicle_range #user sets the range for their vehicle
        self.G = self.create_graph() #read in the graph
        self.refill_locations = self.stations#read in the df. Make sure that refill_locations is used throughout this class!
        self.graph_type = graph_type
        print('Region: '+self.region)        
        
    #getter
    def get_G(self):
        return(self.G)
    
    def source_destination(self):
        #TODO: move the source/destination checking to the first step! This will make it faster...
        return(None)
        
    #this probably isnt needed. All start/end user input should be verified in the Data class
    def available_cities(self):
        cities = list(self.refill_locations['city'].unique())
        return(cities)
        
        
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
        
            
    def shortest_path(self):
        
        source,target = self.start_node,self.end_node
        self.vehicle_route()
  
        #TODO: make sure that self.G has been properly filtered!
        path_data = {}
        path_data['fuel'] = self.vehicle_fuel
        path_data['region'] = self.region
        path_data['user input start'] = self.start
        path_data['user input end'] = self.end
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
        
        return(path_data) #TODO: round everything...
    
        
#%%
if __name__ == "__main__":
    
    Data.create_pickes(max_range=500,min_range=50,graph_type='ny_pickles')
    
    #path = VehicleNetwork(vehicle_fuel='ELEC',start='Calgary,ab',end='London,on',vehicle_range=250)

    #route = path.shortest_path()
    
    #file = Data(vehicle_fuel='ELEC',start='Calgary,ab',end='London,on',graph_type = 'nx_pickles').FileName()
    
#%%

