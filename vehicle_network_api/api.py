from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from vehicle_network import VehicleNetwork

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)
initpath = VehicleNetwork(vehicle_fuel="ELEC", region="CA", vehicle_range=300)


class VehicleRouteService(Resource):

    def get(self, f_type, start_city, end_city, vehicle_range, region, return_cities, return_range):
        if return_cities == "yes":
            return initpath.available_cities()
        elif return_range == "yes":
            return initpath.vehicle_range
        else:
            return initpath.shortest_path(start_city, end_city)


    def put(self, f_type, start_city, end_city, vehicle_range, region, return_cities, return_range):
        newpath = VehicleNetwork(
            vehicle_fuel=f_type,
            region=region,
            vehicle_range=int(vehicle_range)
        )
        global initpath
        initpath = newpath


api.add_resource(
    VehicleRouteService, "/api/<f_type>/<start_city>/<end_city>/<vehicle_range>/<region>/<return_cities>/<return_range>"
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
