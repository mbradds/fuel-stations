const baseUrl =
  process.env.NODE_ENV === "production"
    ? "https://vehicle-network-api.azurewebsites.net/"
    : "http://localhost:5000/";

async function sendFetch(url: string, method: string) {
  try {
    const response = await fetch(url, {
      method,
      credentials: "include",
      headers: {
        accepts: "application/json",
      },
    });
    const data = await response.json();
    return data;
  } catch (err) {
    return err;
  }
}

export async function setInitialRoute() {
  const url = `${baseUrl}api/setInitialRoute`;
  const response = await sendFetch(url, "GET");
  return response;
}

export async function getRoute(startCity: string, endCity: string) {
  const url = `${baseUrl}api/getRoute/${startCity}/${endCity}`;
  const response = await sendFetch(url, "GET");
  return response;
}

export async function updateNetwork(
  fuelType: string,
  vehicleRange: number,
  region: string
) {
  const url = `${baseUrl}api/updateNetwork/${fuelType}/${vehicleRange}/${region}`;
  const response = await sendFetch(url, "PUT");
  return response;
}

export async function getCityOptions() {
  const url = `${baseUrl}api/getCityOptions`;
  const response = await sendFetch(url, "GET");
  return response;
}

export async function getVehicleRange() {
  const url = `${baseUrl}api/getVehicleRange`;
  const response = await sendFetch(url, "GET");
  return response;
}
