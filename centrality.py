#test importing classes
from nrel import Data
stations = Data(vehicle_fuel='ELEC',custom='CA')
G = stations.create_graph()
df = stations.get_stations()