#import nrel
import nrel as path

car = path.VehicleNetwork(vehicle_fuel = 'ELEC',vehicle_range=200,limit=False)
route = car.shortest_path(start='Vancouver',end='Halifax')