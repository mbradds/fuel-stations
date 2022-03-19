import "bootstrap/dist/js/bootstrap.bundle.min.js";
// import { BaseMap } from "./modules/BaseMap";
import { setInitialRoute, getCityOptions } from "./modules/routeData";
import "leaflet/dist/leaflet.css";
import "./css/main.css";

// function setUpMap() {
//   const map = new BaseMap("map", {
//     zoomDelta: 0.5,
//     zoomSnap: 0.5,
//     initZoomLevel: 4,
//     zoomControl: true,
//   });
//   map.addOptionFormHtml();
//   return map;
// }

async function main() {
  // await setInitialRoute().then((response) => {
  //   console.log(JSON.stringify(response));
  //   const map = setUpMap();
  //   const cityOptions = getCityOptions();
  //   map.populateCityDropDowns(cityOptions);
  // });
  await setInitialRoute();
  const cityOptions = await getCityOptions();
  console.log(cityOptions);
}

main();
