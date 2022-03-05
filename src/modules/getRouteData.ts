export async function getRouteData(
  fuelType: string,
  startCity: string,
  endCity: string,
  vehicleRange: number,
  region: string
) {
  try {
    const url = `http://10.0.0.128:5000/api/${fuelType}/${startCity}/${endCity}/${vehicleRange}/${region}`;
    const response = await fetch(url);
    const data = await response.json();
    return data;
  } catch (err) {
    return err;
  }
}
