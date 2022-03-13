from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from waitress import serve
import psutil
import os
from util import set_cwd_to_script
from vehicle_network import VehicleNetwork

set_cwd_to_script()
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)
process = psutil.Process(os.getpid())
initpath = VehicleNetwork(vehicle_fuel="ELEC", region="CA", vehicle_range=300)


class VehicleRouteService(Resource):

    def get(self, start_city, end_city):
        return initpath.shortest_path(start_city, end_city)


class UpdateNetworkService(Resource):

    def put(self, f_type, vehicle_range, region):
        global initpath
        initpath = VehicleNetwork(
            vehicle_fuel=f_type,
            region=region,
            vehicle_range=int(vehicle_range)
        )
        return {"new_fuel": f_type, "new_range": vehicle_range, "new_region": region}


class AvailableCitiesService(Resource):

    def get(self):
        return initpath.available_cities()


class VehicleRangeService(Resource):

    def get(self):
        return initpath.vehicle_range


class PrintMemory(Resource):

    def get(self):
        return {'memory': process.memory_info().rss}


api.add_resource(
    VehicleRouteService, "/api/getRoute/<start_city>/<end_city>"
)

api.add_resource(
    UpdateNetworkService, "/api/updateNetwork/<f_type>/<vehicle_range>/<region>"
)

api.add_resource(
    AvailableCitiesService, "/api/getCityOptions"
)

api.add_resource(
    VehicleRangeService, "/api/getVehicleRange"
)

api.add_resource(
    PrintMemory, "/api/memory"
)

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)
