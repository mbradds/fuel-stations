# fuel-stations

Work in progress. The purpose of this app is to provide an easy to use interface for evaluating if its possible to travel between two different cities in an electric vehicle (EV). Range anxiety is a well known barrier to mass EV adoption, so something like this can be used to evaluate whether your favorite road trips are possible given your vehicles range and the current state of the EV charging network.

## Development instructions

Start the flask api:

```bash
conda activate fuel-stations
cd vehicle_network_api && python3 api.py
```

Start the front end:

```bash
npm run dev
```
