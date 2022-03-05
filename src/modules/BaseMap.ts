import * as L from "leaflet";

interface Config {
  zoomDelta: number;
  zoomSnap: number;
  initZoomTo: L.LatLng;
  initZoomLevel: number;
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
    const resetControl = new L.Control({ position: "bottomleft" });
    const resetId = this.resetBtnId;
    resetControl.onAdd = function resetOnAdd() {
      const resetDiv = L.DomUtil.create("div");
      resetDiv.innerHTML = `<button id="${resetId}" type="button" class="btn btn-secondary btn-lg">Reset Map</button>`;
      return resetDiv;
    };
    resetControl.addTo(this);
    this.resetListener();
  }
}
