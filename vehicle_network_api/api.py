from flask import Flask, session
from flask_session import Session
import json
from flask_cors import CORS
from waitress import serve
import psutil
import os
import sys
from util import set_cwd_to_script
from vehicle_network import VehicleNetwork

set_cwd_to_script()
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
sess = Session()
CORS(app,
     origins=["http://localhost:8080"],
     expose_headers=['Access-Control-Allow-Origin'],
     supports_credentials=True)
app.secret_key = 'supersecretkey'
sess.init_app(app)
process = psutil.Process(os.getpid())


@app.route("/api/setInitialRoute", methods=["GET"])
def set_initial_route():
    if not "initpath" in session:
        session["initpath"] = VehicleNetwork(
            vehicle_fuel="ELEC", region="CA", vehicle_range=300)
        print("session path set", file=sys.stdout)
    else:
        session["initpath"] = session.get("initpath")
    return 'ok'


@app.route("/api/getRoute/<start_city>/<end_city>")
def get_route(start_city, end_city):
    return json.dumps(session.get("initpath").shortest_path(start_city, end_city))


@app.route("/api/updateNetwork/<f_type>/<vehicle_range>/<region>", methods=["PUT"])
def update_network(f_type, vehicle_range, region):
    session["initpath"] = VehicleNetwork(
        vehicle_fuel=f_type,
        region=region,
        vehicle_range=int(vehicle_range)
    )
    return json.dumps({"new_fuel": f_type, "new_range": vehicle_range, "new_region": region})


@app.route("/api/getCityOptions", methods=["GET"])
def get_city_options():
    return json.dumps(session.get("initpath").available_cities())


@app.route("/api/getVehicleRange")
def get_vehicle_range():
    return json.dumps(session.get("initpath").vehicle_range)


@app.route("/api/memory")
def get_memory():
    return {'memory': process.memory_info().rss}


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=5000, debug=True)
    serve(app, host="0.0.0.0", port=5000)
