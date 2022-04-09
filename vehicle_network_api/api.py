from flask import Flask
import json
from flask_cors import CORS
from waitress import serve
import psutil
import os
from util import set_cwd_to_script
from vehicle_network import VehicleNetwork

set_cwd_to_script()
app = Flask(__name__)
CORS(app,
     origins="*",
     expose_headers=['Access-Control-Allow-Origin'],
     supports_credentials=True)
process = psutil.Process(os.getpid())

path = VehicleNetwork(
    vehicle_fuel="ELEC", region="CA", vehicle_range=300)


@app.route("/api/setInitialRoute", methods=["GET"])
def set_initial_route():
    return "ok"


@app.route("/api/getRoute/<start_city>/<end_city>")
def get_route(start_city, end_city):
    return json.dumps(path.shortest_path(start_city, end_city))


@app.route("/api/updateNetwork/<f_type>/<vehicle_range>/<region>", methods=["PUT"])
def update_network(f_type, vehicle_range, region):
    global path
    path = VehicleNetwork(
        vehicle_fuel=f_type,
        region=region,
        vehicle_range=int(vehicle_range)
    )
    return json.dumps({"new_fuel": f_type, "new_range": vehicle_range, "new_region": region})


@app.route("/api/getCityOptions", methods=["GET"])
def get_city_options():
    return json.dumps(path.available_cities())


@app.route("/api/getVehicleRange")
def get_vehicle_range():
    return json.dumps(path.vehicle_range)


@app.route("/api/memory")
def get_memory():
    return {'memory': process.memory_info().rss}


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)
