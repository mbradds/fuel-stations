export async function routeData(
  fuelType: string,
  startCity: string,
  endCity: string,
  vehicleRange: number,
  region: string,
  method: string
) {
  try {
    const url = `http://10.0.0.128:5000/api/${fuelType}/${startCity}/${endCity}/${vehicleRange}/${region}`;
    const response = await fetch(url, { method: method });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}

export async function getCityOptions() {
  try {
    const url = `http://10.0.0.128:5000/api/getCityOptions`;
    const response = await fetch(url, { method: "GET" });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}

export async function getVehicleRange() {
  try {
    const url = `http://10.0.0.128:5000/api/getVehicleRange`;
    const response = await fetch(url, { method: "GET" });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}
