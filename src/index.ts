import * as L from "leaflet";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import { BaseMap } from "./modules/BaseMap";
import { getCityOptions } from "./modules/routeData";
import "leaflet/dist/leaflet.css";
import "./css/main.css";

function setUpMap() {
  const map = new BaseMap("map", {
    zoomDelta: 0.5,
    zoomSnap: 0.5,
    initZoomLevel: 4,
    zoomControl: true,
  });
  map.addOptionFormHtml();
  return map;
}

async function main() {
  const map = setUpMap();
  const cityOptions = getCityOptions();
  map.populateCityDropDowns(cityOptions);
}

main();
