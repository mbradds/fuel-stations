export async function routeData(
  fuelType: string,
  startCity: string,
  endCity: string,
  vehicleRange: number,
  region: string,
  returnCities: string,
  method: string
) {
  try {
    const url = `http://10.0.0.128:5000/api/${fuelType}/${startCity}/${endCity}/${vehicleRange}/${region}/${returnCities}`;
    const response = await fetch(url, { method: method });
    const data = await response.json();
    const objData = JSON.parse(data);
    return objData;
  } catch (err) {
    return err;
  }
}

// export async function putRouteData(
//   fuelType: string,
//   startCity: string,
//   endCity: string,
//   vehicleRange: number,
//   region: string,
//   returnCities: string
// ) {
//   try {
//     const url = `http://10.0.0.128:5000/api/${fuelType}/${startCity}/${endCity}/${vehicleRange}/${region}/${returnCities}`;
//     const response = await fetch(url, { method: "PUT" });
//     const data = await response.json();
//     const objData = JSON.parse(data);
//     return objData;
//   } catch (err) {
//     return err;
//   }
// }
