import networkx as nx
import random
import warnings
import json
import copy
import time
from graph_data import Data


class VehicleNetwork(Data):
    '''
    Fuel Types: ELEC - Electric vehicle, LPG - Propane vehicle, BD - Biodiesel, CNG - compresses natural gas
    this creates a comlete graph, meaning that all vehicle routes are possible. This network will be pruned when the
    user enters in a range for their vehicle. I think this may be faster, especially if each Vehicle_Network is saved and imported
    when needed
    '''

    def __init__(self, vehicle_fuel, region, vehicle_range):
        Data.__init__(self, vehicle_fuel=vehicle_fuel, region=region)
        self.vehicle_fuel = vehicle_fuel #user must select one fuel type.
        self.vehicle_range = vehicle_range
        self.G = self.create_graph() #read in the graph
        print('Region: '+self.region)


    def find_region(self, start, end):
        df = self.stations

        def get_random_location(loc, df):
            df = df[df["city"] == loc].copy()
            unique = [str(c).title() + "_" + str(p) for c, p in zip(df["city"], df["zip"])]
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
            
            input_city = l[0].replace("_", " ")
            input_state = l[1]
            c = df.copy()
            c["city"] = [str(x).lower() for x in c["city"]]
            c["state"] = [str(x).lower() for x in c["state"]]

            try:
                if l[1] == None:
                    location = c[c["city"] == input_city]
                else:
                    location = c[(c["city"] == input_city) & (c["state"] == input_state)]
            except:
                # raise an error. No stations could be found
                location = None

            # get a random station ("node")
            node = get_random_location(input_city, location)

            station_count = {}
            max_stations = 0
            for r in list(location["country"].unique()):
                number_of_stations = len(location[location["country"] == r])
                if number_of_stations > max_stations:
                    max_stations = number_of_stations

                station_count[number_of_stations] = r

            return station_count[max_stations], node


        if self.region != None:
            start_country, start_node = split_location(start)
            end_country, end_node = split_location(end)
            if start_country == end_country:
                r = start_country
            else:
                r = 'NA'
        else:
            r = self.region
            start_node, end_node = None, None

        if r != "NA":
            df = df[df["country"] == r].copy()
        
        start_node = start_node.replace(" ", "_")
        end_node = end_node.replace(" ", "_")
        return start_node, end_node


    # this probably isnt needed. All start/end user input should be verified in the Data class
    def available_cities(self):
        options = [city+","+state for city, state in zip(self.stations["city"], self.stations["state"])]
        options = sorted(list(set(options)))
        return json.dumps(options)
    
    
    def vehicle_route(self):
        remove_list = []
        for paths in self.G.edges(data=True):
            n1 = paths[0]
            n2 = paths[1]
            distance = paths[2]["weight"]
            if distance > self.vehicle_range:
                remove_list.append(tuple((n1, n2)))
        
        self.G.remove_edges_from(remove_list)
        return self.G


    def vehicle_route_trimmed(self):
        remove_list = []
        for paths in self.G.edges(data=True):
            distance = paths[2]["weight"]
            if distance < self.vehicle_range:
                remove_list.append(paths)
        
        trimmed_graph = nx.Graph()
        trimmed_graph.add_nodes_from(self.G.nodes(data=True))
        trimmed_graph.add_edges_from(remove_list)
        return trimmed_graph


    def shortest_path(self, start, end):
        source, target = self.find_region(start, end)
        trimmed_graph = self.vehicle_route()

        # TODO: make sure that self.G has been properly filtered!
        path_data = {}
        path_data["fuel"] = self.vehicle_fuel
        path_data["region"] = self.region
        path_data["start"] = start
        path_data["end"] = end
        path_data["vehicle_range"] = self.vehicle_range

        try:
            path = nx.shortest_path(trimmed_graph, source=source, target=target)
            path_data_detail = []
            cumulative_distance, weight = 0, 0
            for stop_number, stop in enumerate(path):
                if stop_number == 0:
                    None
                elif stop_number < len(path):
                    weight = trimmed_graph[path[stop_number - 1]][path[stop_number]]["weight"]
                    cumulative_distance = cumulative_distance + weight
                else:
                    None

                attributes = trimmed_graph.nodes[stop]
                path_data_detail.append(
                    {
                        "node": stop,
                        "lat": attributes["lat"],
                        "lng": attributes["long"],
                        "city": attributes["city"],
                        "ev_pricing": attributes["ev_pricing"],
                        "facility_type": attributes["facility_type"],
                        "address": attributes["address"],
                        "province": attributes["province"],
                        "station_name": attributes["station_name"],
                        "cumulative_distance": cumulative_distance,
                        "distance_from_prev_node": weight,
                    }
                )

            path_data["total_distance"] = cumulative_distance
            path_data["detailed_path"] = path_data_detail
            path_data["route_found"] = True
        except nx.NetworkXNoPath:
            path_data["route_found"] = False
            path_data["detailed_path"] = None
            path_data["total_distance"] = None
            # TODO: raise a warning that the route didnt work, and then inform the user that a new path is being calculated with a higher range!

        path_data = json.dumps(path_data)
        return path_data  # TODO: round everything...


if __name__ == "__main__":
    start = time.time()
    path = VehicleNetwork(vehicle_fuel='ELEC', region="NA", vehicle_range=300)
    # g = path.G
    # print(g.nodes)
    route = path.shortest_path(start='Vancouver,BC', end='Calgary,AB')
    elapsed = (time.time() - start)
    print("Route process time:", round(elapsed, 0), ' seconds')
    
    # path = VehicleNetwork(vehicle_fuel="ELEC" , region="CA")
    # cities = path.available_cities()


