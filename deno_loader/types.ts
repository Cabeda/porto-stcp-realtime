export interface StopRealtime {
  stopId: string;
  gtfsId: string;
  lat: number;
  lon: number;
  name: string;
  desc: null;
  zoneId: string;
  serviceDay: number;
  realtimeState: string;
  realtimeDeparture: number;
  scheduledDeparture: number;
  realtimeArrival: number;
  scheduledArrival: number;
  arrivalDelay: number;
  departureDelay: number;
  realtime: boolean;
  pickupType: string;
  headsign: string;
  trip_id: string;
  trip_gtfsId: string;
  trip_directionId: string;
  trip_tripHeadsign: string;
  route_id: string;
  route_gtfsId: string;
  route_shortName: string;
  route_longName: string;
  route_mode: string;
  route_color: string;
  agency_name: string;
  agency_id: string;
}

export interface Stop {
  id: string;
  gtfsId: string;
  lat: number;
  lon: number;
  name: string;
  _stoptimesWithoutPatterns24f6Pa: StopTime[];
  desc: null;
  zoneId: string;
}

export interface StopTime {
  serviceDay: number;
  realtimeState: string;
  realtimeDeparture: number;
  scheduledDeparture: number;
  realtimeArrival: number;
  scheduledArrival: number;
  arrivalDelay: number;
  departureDelay: number;
  realtime: boolean;
  pickupType: string;
  headsign: string;
  stop: {
    id: string;
    code: string;
    platformCode: null;
  };
  trip: {
    gtfsId: string;
    directionId: string;
    tripHeadsign: string;
    stops: {
      id: string;
    }[];
    pattern: {
      route: {
        gtfsId: string;
        shortName: string;
        longName: string;
        mode: string;
        color: string;
        agency: {
          name: string;
          id: string;
        };
        id: string;
      };
      code: string;
      stops: {
        gtfsId: string;
        code: string;
        id: string;
      }[];
      id: string;
    };
    id: string;
  };
}

export interface Data {
  stops: Stop[];
}

export interface APIResponse {
  data: Data;
  errors: any[];
}
