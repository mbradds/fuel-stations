export async function getRoute(startCity: string, endCity: string) {
  try {
    const url = `http://10.0.0.128:5000/api/getRoute/${startCity}/${endCity}`;
    const response = await fetch(url, { method: "GET" });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}

export async function updateNetwork(
  fuelType: string,
  vehicleRange: number,
  region: string
) {
  try {
    const url = `http://10.0.0.128:5000/api/updateNetwork/${fuelType}/${vehicleRange}/${region}`;
    const response = await fetch(url, { method: "PUT" });
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
