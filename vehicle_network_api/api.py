from flask import Flask
import pickle
import redis
import json
from flask_cors import CORS
from waitress import serve
import psutil
import os
from util import set_cwd_to_script
from vehicle_network import VehicleNetwork

set_cwd_to_script()
app = Flask(__name__)
r = redis.Redis(host='localhost', port=6379, db=0)
CORS(app,
     origins=["http://localhost:8080"],
     expose_headers=['Access-Control-Allow-Origin'],
     supports_credentials=True)
process = psutil.Process(os.getpid())


@app.route("/api/setInitialRoute", methods=["GET"])
def set_initial_route():
    path = pickle.loads(r.get("initpath"))
    if not path:
        path = VehicleNetwork(
            vehicle_fuel="ELEC", region="CA", vehicle_range=300)
        r.set("initpath", pickle.dumps(path))
        r.set("currentpath", pickle.dumps(path))
        print("initial path set")
    else:
        print("initial path already set")
        r.set("currentpath", pickle.dumps(path))
    return "ok"


@app.route("/api/getRoute/<start_city>/<end_city>")
def get_route(start_city, end_city):
    path = pickle.loads(r.get("currentpath"))
    return json.dumps(path.shortest_path(start_city, end_city))


@app.route("/api/updateNetwork/<f_type>/<vehicle_range>/<region>", methods=["PUT"])
def update_network(f_type, vehicle_range, region):
    newpath = VehicleNetwork(
        vehicle_fuel=f_type,
        region=region,
        vehicle_range=int(vehicle_range)
    )
    r.set("currentpath", pickle.dumps(newpath))
    return json.dumps({"new_fuel": f_type, "new_range": vehicle_range, "new_region": region})


@app.route("/api/getCityOptions", methods=["GET"])
def get_city_options():
    path = pickle.loads(r.get("currentpath"))
    return json.dumps(path.available_cities())


@app.route("/api/getVehicleRange")
def get_vehicle_range():
    path = pickle.loads(r.get("currentpath"))
    return json.dumps(path.vehicle_range)


@app.route("/api/memory")
def get_memory():
    return {'memory': process.memory_info().rss}


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)
