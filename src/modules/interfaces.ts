export interface RouteApiResponse {
  detailed_path: {
    node: string;
    lat: number;
    lng: number;
    address: string;
    city: string;
    cumulative_distance: number;
    distance_from_prev_node: number;
    ev_pricing: string;
    facility_type: string;
    province: string;
    station_name: string;
  }[];
  end: string;
  fuel: string;
  route_found: boolean;
  start: string;
  total_distance: number;
  vehicle_range: number;
}
