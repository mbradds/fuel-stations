import requests
import pandas as pd
import numpy as np
import os
import json
import networkx as nx
from math import radians, cos, sin, asin, sqrt
from itertools import combinations
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Data:
    # TODO: use setter on region depending on start and end values.
    """
    NREL API documentation: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/
    """

    country_options = ['CA','US']

    def __init__(self,
                 vehicle_fuel,
                 max_range = 500,
                 min_range = 50,
                 nrel_data='fuel_stations.csv',
                 region=None):

        self.vehicle_fuel = vehicle_fuel
        self.nrel_data = nrel_data
        self.max_range = max_range
        self.min_range = min_range
        self.region = region
        self.stations = self.get_stations()


    @staticmethod
    def get_config_file(config_file):
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname("__file__")))
        try:
            with open(os.path.join(__location__, config_file)) as f:
                config = json.load(f)
                return config

        except:
            raise


    @staticmethod
    def api_url(key,country,url="https://developer.nrel.gov/api/alt-fuel-stations/v1.json?country=CO&api_key=YOUR_KEY_HERE",):
        url = url.replace("YOUR_KEY_HERE", key)
        url = url.replace("CO", country)
        return url


    @staticmethod
    def request_api(url):
        r = requests.get(url, allow_redirects=True, stream=True, headers=headers).json()  # returns a dictionary
        df = pd.DataFrame(r["fuel_stations"])
        return df


    @staticmethod
    def create_pickes(max_range, min_range):
        fuel_options = ["ELEC", "LPG"] # , "CNG"]  # TODO: add fuel_options to self
        # Data.country_options.append("NA")
        for fuel in fuel_options:
            for country in Data.country_options:
                network = Data(vehicle_fuel=fuel, region=country)
                network.create_graph()


    def file_name(self):
        return('nx_pickles/'+self.vehicle_fuel+'_'+self.region+'_'+'Max_'+str(self.max_range)+'_'+'Min_'+str(self.min_range)+'.pickle')


    def get_stations(self):
        if os.path.isfile(self.nrel_data):
            used_cols = ["city", "zip", "country", "ev_pricing", "facility_type", "fuel_type_code", "latitude", "longitude", "state", "station_name", "street_address"]
            stations = pd.read_csv(self.nrel_data, low_memory=False)
            for col in stations:
                if col not in used_cols:
                    del stations[col]
                else:
                    stations[col] = stations[col].replace({np.nan: None})

        else:
            key = Data.get_config_file("api_key.json")["key"]
            # get both countries
            country_frames = []
            for country in self.country_options:
                url = Data.api_url(key, country)
                print("api request: " + str(url))
                df = Data.request_api(url)
                country_frames.append(df)

            stations = pd.concat(country_frames, axis=0, sort=False, ignore_index=True)
            stations.to_csv(self.nrel_data, index=False)

        stations = stations[stations["fuel_type_code"] == self.vehicle_fuel]
        if self.region != None:
            if self.region != 'NA':
                stations = stations[stations["country"] == self.region].copy()
                
        stations = stations.replace({np.nan: None})
        return stations



    # from https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    def haversine(self, lon1, lat1, lon2, lat2):
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
        return (int(round(c * r,0)))


    def create_graph(self):
        print('called create_graph')
        '''
        creates a semi-complete graph if there isnt already one available in binary form. The graph connectivity is limited by the maximum range.
        A higher max range allows you to view hypothetical vehicle routes that are not available with current EV technology, but it makes the
        optimal path calculation much slower.
        '''
        # TODO: look at casting types for node attributes and edge weight. This may reduce pickle file size
        # TODO: remove limit instance variable after testing is complete!

        file_name = self.file_name()

        if os.path.isfile(file_name):
            G = nx.read_gpickle(file_name)
            print("read pickle object: " + file_name)
        else:
            # ceates a complete graph if there isnt one already
            print("creating pickle object: " + file_name)
            print("DF length: " + str(len(self.stations)))
            G = nx.Graph()
            for index, row in self.stations.iterrows():
                # TODO: add more descriptors (columns) to the graph if neccecary
                G.add_node(
                    str(row["city"]) + "_" + str(row["zip"]),
                    city=row["city"],
                    country=row["country"],
                    ev_pricing=row["ev_pricing"],
                    facility_type=row["facility_type"],
                    fuel=row["fuel_type_code"],
                    lat=row["latitude"],
                    long=row["longitude"],
                    province=row["state"],
                    station_name=row["station_name"],
                    address=row["street_address"],
                )

            # add the graph edges
            print("Nodes: " + str(len(G.nodes)))
            edges = list(combinations(list(G.nodes), 2))
            print("Edges: " + str(len(edges)))

            for edge in edges:
                lat1, long1 = G.nodes[edge[0]]["lat"], G.nodes[edge[0]]["long"]
                lat2, long2 = G.nodes[edge[1]]["lat"], G.nodes[edge[1]]["long"]
                distance = self.haversine(long1, lat1, long2, lat2)
                # there is no range requirement

                if distance > self.max_range or distance < self.min_range:
                    None  # the vehicle cant make it from node 1 to node 2
                else:
                    G.add_edge(edge[0], edge[1], weight=distance)

            # pickle the graph once it is created
            nx.write_gpickle(G, file_name)
            print("created new pickle object: "+ file_name+ " with max range "+ str(self.max_range))
        return G


if __name__ == "__main__":
    # data = Data("ELEC", region="CA")
    Data.create_pickes(500, 50)
    # df = data.get_stations()

