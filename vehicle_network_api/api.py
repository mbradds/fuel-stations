from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from vehicle_network import VehicleNetwork

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)
initpath = VehicleNetwork(vehicle_fuel="ELEC", region="CA", vehicle_range=300)


class VehicleRouteService(Resource):

    def __init__(self, f_type="ELEC", region="CA", vehicle_range=300):
        self.f_type = "ELEC"
        self.region = "CA"
        self.vehicle_range = 300

    def get(self, f_type, start_city, end_city, vehicle_range, region, return_cities):
        if return_cities == "yes":
            return initpath.available_cities()
        else:
            return initpath.shortest_path(start_city, end_city)


    def put(self, f_type, start_city, end_city, vehicle_range, region, return_cities):
        newpath = VehicleNetwork(
            vehicle_fuel=f_type,
            region=region,
            vehicle_range=int(vehicle_range)
        )
        global initpath
        initpath = newpath
        # return initpath


api.add_resource(
    VehicleRouteService, "/api/<f_type>/<start_city>/<end_city>/<vehicle_range>/<region>/<return_cities>"
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
