import { DB, PreparedQuery } from "https://deno.land/x/sqlite/mod.ts";

import { APIResponse, StopRealtime } from "./types.ts";

function initDB(db: DB): PreparedQuery {
  db.execute("create table if not exists stops_history_raw (data json)");

  db.execute(`CREATE TABLE if not exists stop_realtime (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stopId TEXT,
    gtfsId TEXT,
    lat REAL,
    lon REAL,
    name TEXT,
    desc TEXT,
    zoneId TEXT,
    serviceDay INTEGER,
    realtimeState TEXT,
    realtimeDeparture INTEGER,
    scheduledDeparture INTEGER,
    realtimeArrival INTEGER,
    scheduledArrival INTEGER,
    arrivalDelay INTEGER,
    departureDelay INTEGER,
    realtime INTEGER,
    pickupType TEXT,
    headsign TEXT,
    trip_id TEXT,
    trip_gtfsId TEXT,
    trip_directionId TEXT,
    trip_tripHeadsign TEXT,
    route_id TEXT,
    route_gtfsId TEXT,
    route_shortName TEXT,
    route_longName TEXT,
    route_mode TEXT,
    route_color TEXT,
    agency_name TEXT,
    agency_id TEXT
  )`);

  return db.prepareQuery(`
  INSERT INTO stop_realtime (
    stopId,
    gtfsId,
    lat,
    lon,
    name,
    desc,
    zoneId,
    serviceDay,
    realtimeState,
    realtimeDeparture,
    scheduledDeparture,
    realtimeArrival,
    scheduledArrival,
    arrivalDelay,
    departureDelay,
    realtime,
    pickupType,
    headsign,
    trip_id,
    trip_gtfsId,
    trip_directionId,
    trip_tripHeadsign,
    route_id,
    route_gtfsId,
    route_shortName,
    route_longName,
    route_mode,
    route_color,
    agency_name,
    agency_id
  ) VALUES (:stopId,:gtfsId,:lat,:lon,:name,:desc,:zoneId,:serviceDay,:realtimeState,:realtimeDeparture,:scheduledDeparture,:realtimeArrival,:scheduledArrival,:arrivalDelay,:departureDelay,:realtime,:pickupType,:headsign,:trip_id,:trip_gtfsId,:trip_directionId,:trip_tripHeadsign,:route_id,:route_gtfsId,:route_shortName,:route_longName,:route_mode,:route_color,:agency_name,:agency_id)
`);
}

async function getStopRealtime(): Promise<APIResponse | undefined> {
  const query = `
    query StopRoute(
      $id_0: String!
      $startTime_1: Long!
      $timeRange_2: Int!
      $numberOfDepartures_3: Int!
    ) {
      stop(id: $id_0) {
        id
        ...F4
      }
    }
    fragment F1 on Stoptime {
      serviceDay
      realtimeState
      realtimeDeparture
      scheduledDeparture
      realtimeArrival
      scheduledArrival
      arrivalDelay
      departureDelay
      realtime
      serviceDay
      pickupType
      headsign
      stop {
        id
        code
        platformCode
      }
      trip {
        gtfsId
        directionId
        tripHeadsign
        stops {
          id
        }
        pattern {
          route {
            gtfsId
            shortName
            longName
            mode
            color
            agency {
              name
              id
            }
            id
          }
          code
          stops {
            gtfsId
            code
            id
          }
          id
        }
        id
      }
    }

    fragment F2 on Stop {
      gtfsId
      name
      desc
      zoneId
      id
    }
    fragment F3 on Stop {
      gtfsId
      _stoptimesWithoutPatterns24f6Pa: stoptimesWithoutPatterns(
        startTime: $startTime_1
        timeRange: $timeRange_2
        numberOfDepartures: $numberOfDepartures_3
        omitCanceled: false
      ) {
        ...F1
      }
      id
      ...F2
    }
    fragment F4 on Stop {
      gtfsId
      lat
      lon
      name
      id
      ...F3
    }
  `;

  const bodyQL = {
    query,
    operationName: "StopRoute",
    variables: {
      id_0: "2:BRRS2",
      startTime_1: new Date().getTime() / 1000, // Epoch time in seconds
      timeRange_2: 43200,
      numberOfDepartures_3: 5,
    },
  };

  const options = {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0",
      Accept: "*/*",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate, br",
      Referer: "https://explore.porto.pt/",
      OTPTimeout: "10000",
      Origin: "https://explore.porto.pt",
      DNT: "1",
      Connection: "keep-alive",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "cross-site",
      "Sec-GPC": "1",
      Pragma: "no-cache",
      "Cache-Control": "no-cache",
    },
    body: JSON.stringify(bodyQL),
  };

  console.log("Fetching data");
  
  const response = await fetch(
    "https://otp.services.porto.digital/otp/routers/default/index/graphql",
    options
  ).catch((err) => console.error(err));

  if (response) {
    const json = (await response.json()) as APIResponse;
    return json;
  }
}

function convertToStopRealtime(response: APIResponse): StopRealtime[] {
  return response.data.stop._stoptimesWithoutPatterns24f6Pa.map((stop) => {
    const stopTime: StopRealtime = {
      stopId: response.data.stop.id,
      gtfsId: response.data.stop.gtfsId,
      trip_id: stop.trip.id,
      trip_gtfsId: stop.trip.gtfsId,
      trip_directionId: stop.trip.directionId,
      trip_tripHeadsign: stop.trip.tripHeadsign,
      route_id: stop.trip.pattern.route.id,
      route_gtfsId: stop.trip.pattern.route.gtfsId,
      route_shortName: stop.trip.pattern.route.shortName,
      route_longName: stop.trip.pattern.route.longName,
      route_mode: stop.trip.pattern.route.mode,
      route_color: stop.trip.pattern.route.color,
      agency_name: stop.trip.pattern.route.agency.name,
      agency_id: stop.trip.pattern.route.agency.id,
      lat: response.data.stop.lat,
      lon: response.data.stop.lon,
      name: response.data.stop.name,
      desc: response.data.stop.desc,
      zoneId: response.data.stop.zoneId,
      serviceDay: stop.serviceDay,
      realtimeState: stop.realtimeState,
      realtimeDeparture: stop.realtimeDeparture,
      scheduledDeparture: stop.scheduledDeparture,
      realtimeArrival: stop.realtimeArrival,
      scheduledArrival: stop.scheduledArrival,
      arrivalDelay: stop.arrivalDelay,
      departureDelay: stop.departureDelay,
      realtime: stop.realtime,
      pickupType: stop.pickupType,
      headsign: stop.headsign,
    };
    return stopTime;
  });
}

function storeResponse(
  db: DB,
  stmt: PreparedQuery,
  stops: StopRealtime[]
): void {
  try {
    db.transaction(() => {
      console.log("Inserting", stops.length, "predictions");

      for (const stop of stops) {
        stmt.execute({
          stopId: stop.stopId,
          gtfsId: stop.gtfsId,
          lat: stop.lat,
          lon: stop.lon,
          name: stop.name,
          desc: stop.desc,
          zoneId: stop.zoneId,
          serviceDay: stop.serviceDay,
          realtimeState: stop.realtimeState,
          realtimeDeparture: stop.realtimeDeparture,
          scheduledDeparture: stop.scheduledDeparture,
          realtimeArrival: stop.realtimeArrival,
          scheduledArrival: stop.scheduledArrival,
          arrivalDelay: stop.arrivalDelay,
          departureDelay: stop.departureDelay,
          realtime: stop.realtime,
          pickupType: stop.pickupType,
          headsign: stop.headsign,
          trip_id: stop.trip_id,
          trip_gtfsId: stop.gtfsId,
          trip_directionId: stop.trip_directionId,
          trip_tripHeadsign: stop.trip_tripHeadsign,
          route_id: stop.route_id,
          route_gtfsId: stop.route_gtfsId,
          route_shortName: stop.route_shortName,
          route_longName: stop.route_longName,
          route_mode: stop.route_mode,
          route_color: stop.route_color,
          agency_name: stop.agency_name,
          agency_id: stop.agency_id,
        });
      }
    });
  } catch (error) {
    console.log(error);
  }
}

async function run(db: DB, stmt: PreparedQuery): Promise<void> {
  const response = await getStopRealtime();
  if (!response) {
    console.log("No result");
  } else {
    const realtime = convertToStopRealtime(response);
    storeResponse(db, stmt, realtime);
  }
}

const db = new DB("stcp.db");
const stmt = initDB(db);
await run(db, stmt);
setInterval( () => run(db, stmt), 5000); // Run every 5 seconds
