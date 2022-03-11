import * as L from "leaflet";
import { getRoute, updateNetwork, getVehicleRange } from "./routeData";
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
  routeNotFoundId: string;
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
    routeNotFoundId = "route-not-found",
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
    this.routeNotFoundId = routeNotFoundId;
    this.vehicleRange = vehicleRange;
    this.markerFeature = markerFeature;
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(this);

    // This fixes greyed out tiles when the page is refreshed
    setTimeout(() => {
      this.invalidateSize(false);
    }, 0);
  }

  resetListener() {
    const resetMapElement = document.getElementById(this.resetBtnId);
    const routeNotFoundElement = document.getElementById(this.routeNotFoundId);
    if (resetMapElement) {
      resetMapElement.addEventListener("click", () => {
        this.clearMarkers();
        this.setView(this.config.initZoomTo, this.config.initZoomLevel);
        if (routeNotFoundElement) {
          routeNotFoundElement.innerHTML = "";
        }
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

  setRangeLabel() {
    const rangeTitleElement = document.getElementById("vehicle-range-title");
    if (rangeTitleElement) {
      rangeTitleElement.innerHTML = `Vehicle Range (${this.vehicleRange} km)`;
    }
  }

  rangeSliderListener() {
    const sliderElement = <HTMLInputElement>(
      document.getElementById(this.rangeId)
    );
    sliderElement.addEventListener("change", () => {
      const displayValue = parseInt(sliderElement.value);
      this.vehicleRange = displayValue;
      this.updateServerGraph();
      this.setRangeLabel();
    });
  }

  async updateServerGraph() {
    this.clearUserMessage();
    this.addLoader();
    this.setUserMessage("alert-primary", "Updating vehicle network");
    const findRouteElement = <any>document.getElementById(this.findRouteId);
    if (findRouteElement) {
      findRouteElement.disabled = true;
    }
    await updateNetwork("ELEC", this.vehicleRange, "CA");
    if (findRouteElement) {
      findRouteElement.disabled = false;
    }
    this.removeLoader();
    this.clearUserMessage();
  }

  async addOptionFormHtml() {
    const optionFormDiv = document.getElementById(this.optionFormId);
    const btnHtml = (id: string, text: string) =>
      `<button id="${id}" type="button" class="btn btn-secondary">${text}</button>`;

    const serverVehicleRange = await getVehicleRange();
    this.vehicleRange = parseInt(serverVehicleRange);
    const rangeHtml = `<div id="range-holder"><label for="${this.rangeId}" class="form-label"><span id="vehicle-range-title">Vehicle Range (${serverVehicleRange} km)</span></label>
    <input type="range" class="form-range" min="50" max="500" value="${this.vehicleRange}" id="${this.rangeId}"></div>`;

    const routeNotFoundHtml = `<div id="${this.routeNotFoundId}"> </div>`;

    if (optionFormDiv) {
      optionFormDiv.innerHTML = `${this.getSpinnerHtml(
        this.selectFromCityId
      )} ${this.getSpinnerHtml(this.selectToCityId)} ${rangeHtml} ${btnHtml(
        this.findRouteId,
        "Find Route"
      )}<div id="${this.loadingId}" ></div>${routeNotFoundHtml}`;
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
    this.rangeSliderListener();
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

      const fromSelect = <any>document.getElementById(this.selectFromCityId);
      const toSelect = <any>document.getElementById(this.selectToCityId);
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

  addLoader() {
    const spinnerElement = document.getElementById(this.loadingId);
    if (spinnerElement) {
      spinnerElement.innerHTML = this.getSpinnerHtml("");
    }
  }

  removeLoader() {
    const spinnerElement = document.getElementById(this.loadingId);
    if (spinnerElement) {
      spinnerElement.innerHTML = "";
    }
  }

  findRouteListener() {
    const findRouteElement = document.getElementById(this.findRouteId);
    const [fromSelect, toSelect] = [
      <any>document.getElementById("fromDatalist"),
      <any>document.getElementById("toDatalist"),
    ];
    if (findRouteElement && fromSelect && toSelect) {
      findRouteElement.addEventListener("click", async () => {
        this.clearMarkers();
        this.clearUserMessage();
        this.addLoader();
        const fromCity = BaseMap.validateInputCity(fromSelect.value);
        const toCity = BaseMap.validateInputCity(toSelect.value);
        if (fromCity !== "" && toCity !== "") {
          const data = await getRoute(fromCity, toCity);
          this.vehicleRange = data.vehicle_range;
          this.setRangeLabel();
          this.addRoute(data);
        } else {
          this.setUserMessage(
            "alert-warning",
            "Please select a start and end city"
          );
        }
        this.removeLoader();
      });
    }
  }

  setUserMessage(alertType: string, message: string) {
    const routeNotFoundElement = document.getElementById(this.routeNotFoundId);
    if (routeNotFoundElement) {
      routeNotFoundElement.innerHTML = `<div class="alert ${alertType} d-flex align-items-center" role="alert">
      <div>
        ${message}
      </div>
    </div>`;
    }
  }

  clearUserMessage() {
    const routeNotFoundElement = document.getElementById(this.routeNotFoundId);
    if (routeNotFoundElement) {
      routeNotFoundElement.innerHTML = "";
    }
  }

  addRoute(routeData: RouteApiResponse) {
    if (routeData.route_found) {
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
      this.setUserMessage("alert-success", "Possible route found");
    } else {
      this.markerFeature = undefined;
      this.setUserMessage(
        "alert-danger",
        "Cant find a route. Try increasing the vehicle range."
      );
    }
  }
}
