// const baseUrl =
//   process.env.NODE_ENV === "production"
//     ? "https://vehicle-network-api.azurewebsites.net/"
//     : "http://10.0.0.128:5000/";

const baseUrl = "http://10.0.0.128:5000/";

export async function setInitialRoute() {
  try {
    const url = `${baseUrl}api/setInitialRoute`;
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
    });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}

export async function getRoute(startCity: string, endCity: string) {
  try {
    const url = `${baseUrl}api/getRoute/${startCity}/${endCity}`;
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
      headers: {
        accepts: "application/json",
      },
    });
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
    const url = `${baseUrl}api/updateNetwork/${fuelType}/${vehicleRange}/${region}`;
    const response = await fetch(url, {
      method: "PUT",
      credentials: "include",
      headers: {
        accepts: "application/json",
      },
    });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}

export async function getCityOptions() {
  try {
    const url = `${baseUrl}api/getCityOptions`;
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
    });
    const data = await response.json();
    return data;
    // const objData = JSON.parse(data);
    // return objData;
  } catch (err) {
    return err;
  }
}

export async function getVehicleRange() {
  try {
    const url = `${baseUrl}api/getVehicleRange`;
    const response = await fetch(url, {
      method: "GET",
      credentials: "include",
      headers: {
        accepts: "application/json",
      },
    });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}
