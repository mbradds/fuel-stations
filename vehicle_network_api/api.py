from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from util import set_cwd_to_script
from vehicle_network import VehicleNetwork

set_cwd_to_script()
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)
initpath = VehicleNetwork(vehicle_fuel="ELEC", region="CA", vehicle_range=300)


class VehicleRouteService(Resource):

    def get(self, f_type, start_city, end_city, vehicle_range, region):
        print("here!")
        return initpath.shortest_path(start_city, end_city)

    def put(self, f_type, start_city, end_city, vehicle_range, region):
        newpath = VehicleNetwork(
            vehicle_fuel=f_type,
            region=region,
            vehicle_range=int(vehicle_range)
        )
        global initpath
        initpath = newpath


class AvailableCitiesService(Resource):

    def get(self):
        return initpath.available_cities()


class VehicleRangeService(Resource):

    def get(self):
        return initpath.vehicle_range


api.add_resource(
    VehicleRouteService, "/api/<f_type>/<start_city>/<end_city>/<vehicle_range>/<region>"
)

api.add_resource(
    AvailableCitiesService, "/api/getCityOptions"
)

api.add_resource(
    VehicleRangeService, "/api/getVehicleRange"
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
