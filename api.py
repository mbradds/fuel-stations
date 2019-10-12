from flask import Flask
from flask_restful import Resource, Api

from nrel import VehicleNetwork

app = Flask(__name__)
api = Api(app)

class EvGraph(Resource):
    def get(self,f_type,start_city,end_city,vehicle_range):
        path = VehicleNetwork(vehicle_fuel=f_type,start=start_city,end=end_city,vehicle_range=int(vehicle_range))
        route = path.shortest_path()
        return route

api.add_resource(EvGraph, "/api/<f_type>/<start_city>/<end_city>/<vehicle_range>")

if __name__ == "__main__":
    app.run(debug=True)
