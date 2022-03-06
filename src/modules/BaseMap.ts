import * as L from "leaflet";
import { RouteApiResponse } from "./interfaces";

L.Icon.Default.imagePath = "./dist/images";
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require("leaflet/dist/images/marker-icon-2x.png"),
  iconUrl: require("leaflet/dist/images/marker-icon.png"),
  shadowUrl: require("leaflet/dist/images/marker-shadow.png"),
});

interface Config {
  zoomDelta: number;
  zoomSnap: number;
  initZoomTo: L.LatLng;
  initZoomLevel: number;
  zoomControl: boolean;
}

export class BaseMap extends L.Map {
  resetBtnId: string;
  config: Config;

  constructor(div: string, config: Config, resetBtnId = "reset-map") {
    super(div, config);
    this.config = config;
    this.setView(config.initZoomTo, config.initZoomLevel);
    this.resetBtnId = resetBtnId;
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this);
  }

  resetListener() {
    const resetMapElement = document.getElementById(this.resetBtnId);
    if (resetMapElement) {
      resetMapElement.addEventListener("click", () => {
        this.setView(this.config.initZoomTo, this.config.initZoomLevel);
      });
    }
  }

  addResetBtn() {
    const resetControl = new L.Control({ position: "topleft" });
    const resetId = this.resetBtnId;
    resetControl.onAdd = function resetOnAdd() {
      const resetDiv = L.DomUtil.create("div", "options-bar");
      const resetHtml = `<button id="${resetId}" type="button" class="btn btn-secondary btn-lg">Reset Map</button>`;
      const cardHtml = `<div class="card"><div class="card-body">${resetHtml}</div></div>`;
      resetDiv.innerHTML = cardHtml;
      return resetDiv;
    };
    resetControl.addTo(this);
    this.resetListener();
  }

  addRoute(routeData: RouteApiResponse) {
    console.log(routeData);
    const markers = routeData.detailed_path.map((stop) => {
      return L.marker([stop.lat, stop.lng], {
        icon: L.icon({
          iconUrl: "./images/marker-icon.png",
          iconAnchor: [10, 40],
        }),
      })
        .bindPopup(`${stop.node}`)
        .addTo(this);
    });
    const markerFeature = new L.FeatureGroup(markers);
    this.flyToBounds(markerFeature.getBounds(), {
      duration: 0.25,
      easeLinearity: 1,
      padding: [25, 25],
    });
    return markerFeature;
  }
}
