from nrel import Location, Data


if __name__ == "__main__":
    # key = Data.config_file("api_key.json")["key"]
    # url = Location.api_url(key, "US")
    # df = Location.request_api(url)
    
    l = Location(vehicle_fuel="ELEC", start="Calgary,ab", end="London,on", region="CA")
    df = l.get_stations()