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
import json
#%%

class Configuration:
    
    max_range = 500
    min_range = 50
      
    def __init__(self, vehicle_fuel, start, end, vehicle_range, nrel_data="fuel_stations.csv"):
        self.vehicle_fuel = vehicle_fuel
        self.nrel_data = nrel_data
        self.start = start
        self.end = end
        self.vehicle_range = vehicle_range
        self.G = None
    
    def get_stations(self):
        # print('called get_stations')
        if os.path.isfile(self.nrel_data):
            stations = pd.read_csv(
                self.nrel_data,
                dtype={
                    "access_code": "object",
                    "access_days_time": "object",
                    "access_detail_code": "object",
                    "cards_accepted": "object",
                    "date_last_confirmed": "object",
                    "expected_date": "object",
                    "fuel_type_code": "object",
                    "groups_with_access_code": "object",
                    "id": "int64",
                    "open_date": "object",
                    "owner_type_code": "object",
                    "status_code": "object",
                    "station_name": "object",
                    "station_phone": "object",
                    "updated_at": "object",
                    "facility_type": "object",
                    "geocode_status": "object",
                    "latitude": "float64",
                    "longitude": "float64",
                    "city": "object",
                    "intersection_directions": "object",
                    "plus4": "float64",
                    "state": "object",
                    "street_address": "object",
                    "zip": "object",
                    "country": "object",
                    "bd_blends": "object",
                    "cng_dispenser_num": "float64",
                    "cng_fill_type_code": "object",
                    "cng_psi": "object",
                    "cng_renewable_source": "object",
                    "cng_total_compression": "float64",
                    "cng_total_storage": "float64",
                    "cng_vehicle_class": "object",
                    "e85_blender_pump": "object",
                    "e85_other_ethanol_blends": "object",
                    "ev_connector_types": "object",
                    "ev_dc_fast_num": "float64",
                    "ev_level1_evse_num": "float64",
                    "ev_level2_evse_num": "float64",
                    "ev_network": "object",
                    "ev_network_web": "object",
                    "ev_other_evse": "object",
                    "ev_pricing": "object",
                    "ev_renewable_source": "object",
                    "hy_is_retail": "object",
                    "hy_pressures": "object",
                    "hy_standards": "object",
                    "hy_status_link": "object",
                    "lng_renewable_source": "float64",
                    "lng_vehicle_class": "object",
                    "lpg_primary": "object",
                    "lpg_nozzle_types": "object",
                    "ng_fill_type_code": "object",
                    "ng_psi": "object",
                    "ng_vehicle_class": "object",
                    "access_days_time_fr": "object",
                    "intersection_directions_fr": "object",
                    "bd_blends_fr": "float64",
                    "groups_with_access_code_fr": "object",
                    "ev_pricing_fr": "object",
                    "ev_network_ids": "object",
                    "federal_agency": "object",
                },
            )
            # print('read file from: '+os.getcwd())
        else:
            print('csv file not found')
        return (stations)

    def find_region(self, custom=None):

        df = self.get_stations()

        def get_random_location(loc, df):

            df = df[df["city"] == loc].copy()
            unique = [str(c).capitalize() + "_" + str(p) for c, p in zip(df["city"], df["zip"])]
            unique = list(set(unique))

            # raise a warning if the size of locations == 0. This means there isnt a station in that city
            if len(unique) == 0:
                warnings.simplefilter("error")
                warnings.warn("There are no " + self.vehicle_fuel + " stations " + "in " + loc)
            # location = locations.sample(n=1) #should be one row of a dataframe
            n = random.choice(unique)

            return n

        def split_location(loc):
            loc = loc.lower()
            l = loc.split(",")
            if len(l) < 2:
                l.append(None)

            c = df.copy()
            c["city"] = [str(x).lower() for x in c["city"]]
            c["state"] = [str(x).lower() for x in c["state"]]

            try:

                if l[1] == None:
                    location = c[c["city"] == l[0]]
                else:
                    location = c[(c["city"] == l[0]) & (c["state"] == l[1])]
            except:
                # raise an error. No stations could be found
                location = None

            # get a random station ("node")

            node = get_random_location(l[0], location)

            station_count = {}
            max_stations = 0
            for r in list(location["country"].unique()):
                number_of_stations = len(location[location["country"] == r])
                if number_of_stations > max_stations:
                    max_stations = number_of_stations

                station_count[number_of_stations] = r

            return (station_count[max_stations], node)

        start_country, start_node = split_location(self.start)
        end_country, end_node = split_location(self.end)

        if custom == None:
            if start_country == end_country:
                r = start_country
                # return(start_country,start_node,end_node)
            else:
                r = "NA"
                # return('NA',start_node,end_node)
        else:
            r = custom

        if r != "NA":
            df = df[df["country"] == r].copy()

        return (r, start_node, end_node, df)
    
    def FileName(self,region):
        return(self.vehicle_fuel+'_'+region+'_'+'Max_'+str(Configuration.max_range)+'_'+'Min_'+str(Configuration.min_range)+'.pickle')

    def default_options(self):
        
        options = {'fuel_type':'ELEC',
                   'vehicle_range':250,
                   'region':'CA'}
        
        if not os.path.isfile('client_selection.json'):
            with open('client_selection.json','w') as outfile:
                json.dump(options,outfile)
    

class Import(Configuration):
    
    
    def __init__(self,vehicle_fuel, start, end, vehicle_range):
        Configuration.__init__(self,vehicle_fuel,start,end,vehicle_range)
        self.region,self.start_node,self.end_node,self.df = self.find_region()
        self.default_options()
        #if self.G == None:
        #    self.G = self.import_pickle(self.region)
        
    def write_client_selection(self):
        options = {'fuel_type':self.vehicle_fuel,
                   'vehicle_range':self.vehicle_range,
                   'region':self.region}
        
        with open('client_selection.json','w') as outfile:
            json.dump(options,outfile)
    
    def read_client_selection(self):
        with open('client_selection.json') as json_file:
            options = json.load(json_file)
        return(options)
    
    def import_graph(self):
        #read in the saved selections
        saved_options = self.read_client_selection()
        saved_fuel,saved_range,saved_region = saved_options['fuel_type'],saved_options['vehicle_range'],saved_options['region']
        
        if (saved_fuel != self.vehicle_fuel) or (saved_range != self.vehicle_range) or (saved_region != self.region):
            import_ = True
            print('import new graph')
            self.write_client_selection()
            #self.G = self.import_pickle(self.region)
        else:
            import_ = False
            print('re-use old graph')
        return(import_)
    
    def import_pickle(self):
        G = nx.read_gpickle('nx_pickles/'+self.FileName(self.region))
        print('read pickle')
        return(G)
    

#%%
if __name__ == "__main__":
    
    #setup = Configuration('ELEC','Calgary','Edmonton',vehicle_range=250)
    #region = setup.find_region()[0]
    #file_name = setup.FileName(region)
    
    setup = Import('LPG','Vancouver','Edmonton',vehicle_range=151)
    region = setup.find_region()[0]
    file_name = setup.FileName(region)
    i = setup.import_graph()






