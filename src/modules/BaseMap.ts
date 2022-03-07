import * as L from "leaflet";
import { routeData } from "./routeData";
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
  loadingId: string;
  rangeId: string;
  vehicleRange: number;
  markerFeature: undefined | L.FeatureGroup;
  config: Config;

  constructor(
    div: string,
    config: Config,
    optionFormId = "map-form",
    resetBtnId = "reset-map",
    selectFromCityId = "select-from-city",
    selectToCityId = "select-to-city",
    findRouteId = "find-route",
    loadingId = "loading-spinner",
    rangeId = "select-range",
    vehicleRange = 300,
    markerFeature = undefined
  ) {
    super(div, config);
    this.config = config;
    this.setView(config.initZoomTo, config.initZoomLevel);
    this.resetBtnId = resetBtnId;
    this.optionFormId = optionFormId;
    this.selectFromCityId = selectFromCityId;
    this.selectToCityId = selectToCityId;
    this.findRouteId = findRouteId;
    this.loadingId = loadingId;
    this.rangeId = rangeId;
    this.vehicleRange = vehicleRange;
    this.markerFeature = markerFeature;
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this);
  }

  resetListener() {
    const resetMapElement = document.getElementById(this.resetBtnId);
    if (resetMapElement) {
      resetMapElement.addEventListener("click", () => {
        this.clearMarkers();
        this.setView(this.config.initZoomTo, this.config.initZoomLevel);
      });
    }
  }

  clearMarkers() {
    if (this.markerFeature) {
      this.markerFeature.eachLayer((marker) => {
        marker.remove();
      });
      this.markerFeature = undefined;
    }
  }

  getSpinnerHtml(id: string) {
    return `<div id="${id}"> <div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>
  `;
  }

  addOptionFormHtml() {
    const optionFormDiv = document.getElementById(this.optionFormId);
    const btnHtml = (id: string, text: string) =>
      `<button id="${id}" type="button" class="btn btn-secondary">${text}</button>`;

    const rangeHtml = `<div id="range-holder"><label for="${this.rangeId}" class="form-label">Vehicle Range</label>
    <input type="range" class="form-range" id="${this.rangeId}"></div>`;

    if (optionFormDiv) {
      optionFormDiv.innerHTML = `${this.getSpinnerHtml(
        this.selectFromCityId
      )} ${this.getSpinnerHtml(this.selectToCityId)} ${rangeHtml} ${btnHtml(
        this.findRouteId,
        "Find Route"
      )}<div id="${this.loadingId}" ></div>`;
    }

    const resetControl = new L.Control({ position: "bottomleft" });
    const resetBtnHtml = btnHtml(this.resetBtnId, "Reset Map");
    resetControl.onAdd = function resetOnAdd() {
      const resetDiv = L.DomUtil.create("div");
      resetDiv.innerHTML = resetBtnHtml;
      return resetDiv;
    };
    resetControl.addTo(this);
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

  static validateInputCity(city: string) {
    return city.replaceAll(" ", "_");
  }

  findRouteListener() {
    const findRouteElement = document.getElementById(this.findRouteId);
    const spinnerElement = document.getElementById(this.loadingId);
    const [fromSelect, toSelect] = [
      <any>document.getElementById("fromDatalist"),
      <any>document.getElementById("toDatalist"),
    ];
    const currentVehicleRange = this.vehicleRange;
    if (findRouteElement && fromSelect && toSelect) {
      findRouteElement.addEventListener("click", async () => {
        this.clearMarkers();
        if (spinnerElement) {
          spinnerElement.innerHTML = this.getSpinnerHtml("");
        }
        const fromCity = BaseMap.validateInputCity(fromSelect.value);
        const toCity = BaseMap.validateInputCity(toSelect.value);
        console.log(fromCity, toCity);
        const data = await routeData(
          "ELEC",
          fromCity,
          toCity,
          currentVehicleRange,
          "CA",
          "no",
          "GET"
        );
        this.addRoute(data);
        if (spinnerElement) {
          spinnerElement.innerHTML = "";
        }
      });
    }
  }

  addRoute(routeData: RouteApiResponse) {
    // console.log(routeData);
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
    this.markerFeature = markerFeature;
  }
}
