from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from nrel import VehicleNetwork

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
api = Api(app)


class VehicleRouteService(Resource):
    def get(self, f_type, start_city, end_city, vehicle_range, region):
        path = VehicleNetwork(
            vehicle_fuel=f_type,
            start=start_city,
            end=end_city,
            vehicle_range=int(vehicle_range),
            region=region
        )
        route = path.shortest_path()
        return route


api.add_resource(
    VehicleRouteService, "/api/<f_type>/<start_city>/<end_city>/<vehicle_range>/<region>"
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
