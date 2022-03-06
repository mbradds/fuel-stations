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
  optionFormId: string;
  selectFromCityId: string;
  selectToCityId: string;
  findRouteId: string;
  config: Config;

  constructor(
    div: string,
    config: Config,
    optionFormId = "map-form",
    resetBtnId = "reset-map",
    selectFromCityId = "select-from-city",
    selectToCityId = "select-to-city",
    findRouteId = "find-route"
  ) {
    super(div, config);
    this.config = config;
    this.setView(config.initZoomTo, config.initZoomLevel);
    this.resetBtnId = resetBtnId;
    this.optionFormId = optionFormId;
    this.selectFromCityId = selectFromCityId;
    this.selectToCityId = selectToCityId;
    this.findRouteId = findRouteId;
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

  addOptionFormHtml() {
    const optionFormDiv = document.getElementById(this.optionFormId);
    const btnHtml = (id: string, text: string) =>
      `<button id="${id}" type="button" class="btn btn-secondary">${text}</button>`;
    const citySelectSpinners = (
      id: string
    ) => `<div id="${id}"> <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>
  `;

    if (optionFormDiv) {
      optionFormDiv.innerHTML = `${citySelectSpinners(
        this.selectFromCityId
      )} ${citySelectSpinners(this.selectToCityId)} ${btnHtml(
        this.findRouteId,
        "Find Route"
      )} ${btnHtml(this.resetBtnId, "ResetMap")}`;
    }
    this.resetListener();
  }

  getSelectElements() {
    const fromSelect = <any>document.getElementById(this.selectFromCityId);
    const toSelect = <any>document.getElementById(this.selectToCityId);
    return [fromSelect, toSelect];
  }

  populateCityDropDowns(promiseList: Promise<string[]>) {
    let optionHtml = "";
    promiseList.then((cities: string[]) => {
      cities.forEach((city) => {
        optionHtml += `<option value="${city}">`;
      });
      const fromHtml = `<input class="form-control" list="fromDatalistOptions" id="fromDatalist" placeholder="Select Start City">
      <datalist id="fromDatalistOptions">
      ${optionHtml}
      </datalist>`;
      const toHtml = `<input class="form-control" list="toDatalistOptions" id="toDatalist" placeholder="Select End City">
      <datalist id="toDatalistOptions">
      ${optionHtml}
      </datalist>`;

      const [fromSelect, toSelect] = this.getSelectElements();
      if (fromSelect && toSelect) {
        fromSelect.innerHTML = fromHtml;
        toSelect.innerHTML = toHtml;
      }
      this.findRouteListener();
    });
  }

  findRouteListener() {
    const findRouteElement = document.getElementById(this.findRouteId);
    const [fromSelect, toSelect] = [
      <any>document.getElementById("fromDatalist"),
      <any>document.getElementById("toDatalist"),
    ];
    if (findRouteElement && fromSelect && toSelect) {
      findRouteElement.addEventListener("click", () => {
        const fromCity = fromSelect.value;
        const toCity = toSelect.value;
        console.log(fromCity, toCity);
      });
    }
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
