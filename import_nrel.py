#import nrel
import nrel as path

car = path.VehicleNetwork(vehicle_fuel = 'ELEC',vehicle_range=200)
route = car.shortest_path(start='Vancouver',end='Halifax')
#%%
