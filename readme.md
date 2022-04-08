# fuel-stations

Work in progress. The purpose of this app is to provide an easy to use interface for evaluating if its possible to travel between two different cities in an electric vehicle (EV). Range anxiety is a well known barrier to mass EV adoption, so something like this can be used to evaluate whether your favorite road trips are possible given your vehicles range and the current state of the EV charging network.

## Run the project locally

1. Clone the repo and cd into the fuel-stations folder.

2. Set up the back end python environment and dependencies

Move to the api sub-folder

```
cd vehicle_network_api
```

create the fuel-stations environment (env)

```bash
pip3 install -r requirements.txt
cd ..
```

3. Set up the front end dependencies

```bash
npm install
```

4. Create the vehicle network files

```bash
npm run build-networks
```

5. Start the backend flask app

```bash
cd vehicle_network_api
source env/bin/activate
cd ..
npm run start-api
```

6. Start the front end dev server

```bash
npm run dev
```

## Reference

Build containers

```bash
docker-compose build
```

Run containers

```bash
docker-compose up
```

Save pip environment

```bash
cd vehicle_network_api
pip3 freeze > requirements.txt
```

Get docker image size

```bash
docker images | grep fuel-stations
```

Current sizes
fuel-stations_vehicle_network_api latest 7b9b040964ee 48 seconds ago 1.6GB
fuel-stations_frontend latest f93bebffb052 7 minutes ago 2.4GB

Python virtual environment (venv)

```bash
cd vehicle_network_api
```

create the environment

```bash
python3 -m venv env
```

Activate the environment

```bash
source env/bin/activate
```

Save environment

```bash
pip freeze > requirements.txt
```
