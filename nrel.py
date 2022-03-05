import networkx as nx
import random
import warnings
from graph_data import Data


class VehicleNetwork(Data):
    '''
    Fuel Types: ELEC - Electric vehicle, LPG - Propane vehicle, BD - Biodiesel, CNG - compresses natural gas
    this creates a comlete graph, meaning that all vehicle routes are possible. This network will be pruned when the
    user enters in a range for their vehicle. I think this may be faster, especially if each Vehicle_Network is saved and imported
    when needed
    '''

    def __init__(self, vehicle_fuel, start, end, vehicle_range, region):
        Data.__init__(self, vehicle_fuel=vehicle_fuel, region=region)
        self.vehicle_fuel = vehicle_fuel #user must select one fuel type.
        self.start = start
        self.end = end
        self.vehicle_range = vehicle_range #user sets the range for their vehicle
        self.G = self.create_graph() #read in the graph
        self.refill_locations = self.stations#read in the df. Make sure that refill_locations is used throughout this class!
        print('Region: '+self.region)


    def find_region(self):
        df = self.stations

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


        if self.region != None:
            start_country, start_node = split_location(self.start)
            end_country, end_node = split_location(self.end)
            if start_country == end_country:
                r = start_country
            else:
                r = 'NA'
        else:
            r = self.region
            start_node, end_node = None, None

        if r != "NA":
            df = df[df["country"] == r].copy()

        return start_node, end_node


    # this probably isnt needed. All start/end user input should be verified in the Data class
    def available_cities(self):
        return list(self.refill_locations["city"].unique())


    def vehicle_route(self):
        remove_list = []
        for paths in self.G.edges(data=True):
            n1 = paths[0]
            n2 = paths[1]
            distance = paths[2]["weight"]

            if distance > self.vehicle_range:
                remove_list.append(tuple((n1, n2)))

        self.G.remove_edges_from(remove_list)


    def shortest_path(self):

        source, target = self.find_region()
        self.vehicle_route()

        # TODO: make sure that self.G has been properly filtered!
        path_data = {}
        path_data["fuel"] = self.vehicle_fuel
        path_data["region"] = self.region
        path_data["user input start"] = self.start
        path_data["user input end"] = self.end
        path_data["vehicle range"] = self.vehicle_range

        try:
            path = nx.shortest_path(self.G, source=source, target=target)
            path_data["route"] = path
            path_data["number of stops"] = len(path)
            # the path variable is a list of nodes. Now access node attributes to get lat/long,etc
            path_data_detail = []
            cumulative_distance, weight = 0, 0
            for stop_number, stop in enumerate(path):
                if stop_number == 0:
                    None
                elif stop_number < len(path):
                    weight = self.G[path[stop_number - 1]][path[stop_number]]["weight"]
                    cumulative_distance = cumulative_distance + weight
                else:
                    None

                attributes = self.G.nodes[stop]
                path_data_detail.append(
                    {
                        stop: {
                            "latitude": attributes["lat"],
                            "longitude": attributes["long"],
                            "fuel": attributes["fuel"],
                            "city": attributes["city"],
                            "ev_pricing": attributes["ev_pricing"],
                            "facility_type": attributes["facility_type"],
                            "address": attributes["address"],
                            "province": attributes["province"],
                            "station_name": attributes["station_name"],
                            "cumulative_distance": cumulative_distance,
                            "distance from previous node": weight,
                        }
                    }
                )

            path_data["total distance"] = cumulative_distance
            path_data["detailed path"] = path_data_detail
            path_data["route found"] = True
        except:
            path_data["route found"] = False
            path_data["detailed path"] = None
            path_data["total distance"] = None
            raise
            # TODO: raise a warning that the route didnt work, and then inform the user that a new path is being calculated with a higher range!

        return path_data  # TODO: round everything...


if __name__ == "__main__":

    # stations = Data(vehicle_fuel='ELEC',min_range=200,max_range=400,custom='CA')
    # G = stations.create_graph()
    # df = stations.get_stations()

    # Data.create_pickes(max_range=500, min_range=50)
    path = VehicleNetwork(vehicle_fuel='ELEC', start='Calgary,ab', end='London,on', vehicle_range=500, region="CA")
    route = path.shortest_path()


