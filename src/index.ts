import * as L from "leaflet";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BaseMap } from "./modules/BaseMap";
import { routeData } from "./modules/routeData";
import "leaflet/dist/leaflet.css";
import "./css/main.css";

function setUpMap() {
  const map = new BaseMap("map", {
    zoomDelta: 1,
    zoomSnap: 0.5,
    initZoomTo: L.latLng(49.9, -97.1),
    initZoomLevel: 4,
    zoomControl: false,
  });
  map.addOptionFormHtml();
  return map;
}

async function main() {
  const map = setUpMap();
  // const data = await routeData(
  //   "ELEC",
  //   "Calgary,ab",
  //   "London,on",
  //   500,
  //   "CA",
  //   "no",
  //   "GET"
  // );
  const cityOptions = routeData(
    "ELEC",
    "None",
    "None",
    500,
    "CA",
    "yes",
    "GET"
  );
  map.populateCityDropDowns(cityOptions);
  // const data = await putRouteData("LPG", "Calgary,ab", "London,on", 500, "US");
  // map.addRoute(data);
}

main();
