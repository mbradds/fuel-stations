import * as L from "leaflet";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BaseMap } from "./modules/BaseMap";
import { getRouteData } from "./modules/getRouteData";
import "leaflet/dist/leaflet.css";
import "./css/main.css";

function setUpMap() {
  const map = new BaseMap("map", {
    zoomDelta: 1,
    zoomSnap: 0.5,
    initZoomTo: L.latLng(49.9, -97.1),
    initZoomLevel: 4,
  });
  map.addResetBtn();
  return map;
}

async function main() {
  const map = setUpMap();
  const data = await getRouteData("ELEC", "Calgary,ab", "London,on", 500, "CA");
  console.log(data);
}

main();
