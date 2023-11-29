{{
    config(
        materialized='table'
    )
}}

with unnested_stops as (
    select
        id,
        name,
        code,
        lat,
        lon,
        "locationType",
        "zoneId",
        "vehicleType",
        "vehicleMode",
        "platformCode",
        "gtfsId",
        "desc",
        UNNEST(_stoptimeswithoutpatterns24f6pa) as stop_times
    from {{ref('trip_stops_raw')}}
)
select 
    unnested_stops.id,
    unnested_stops.name,
    unnested_stops.code,
    unnested_stops.lat,
    unnested_stops.lon,
    unnested_stops."locationType",
    unnested_stops."zoneId",
    unnested_stops."vehicleType",
    unnested_stops."vehicleMode",
    unnested_stops."platformCode",
    unnested_stops."gtfsId",
    unnested_stops."desc",
    unnested_stops.stop_times.stop.id as stopId,
    unnested_stops.stop_times.serviceDay as serviceDay,
    unnested_stops.stop_times.realtimeState as realtimeState,
    unnested_stops.stop_times.realtimeDeparture as realtimeDeparture,
    unnested_stops.stop_times.scheduledDeparture as scheduledDeparture,
    unnested_stops.stop_times.realtimeArrival as realtimeArrival,
    unnested_stops.stop_times.scheduledArrival as scheduledArrival,
    unnested_stops.stop_times.arrivalDelay as arrivalDelay,
    unnested_stops.stop_times.departureDelay as departureDelay,
    unnested_stops.stop_times.realtime as realtime,
    unnested_stops.stop_times.pickupType as pickupType,
    unnested_stops.stop_times.headsign as headsign,
    unnested_stops.stop_times.trip.id as trip_id,
    unnested_stops.stop_times.trip.gtfsId as trip_gtfsId,
    unnested_stops.stop_times.trip.directionId as trip_directionId,
    unnested_stops.stop_times.trip.tripHeadsign as trip_tripHeadsign,
    unnested_stops.stop_times.trip.pattern.route.id as route_id,
    unnested_stops.stop_times.trip.pattern.route.gtfsId as route_gtfsId,
    unnested_stops.stop_times.trip.pattern.route.shortName as route_shortName,
    unnested_stops.stop_times.trip.pattern.route.longName as route_longName,
    unnested_stops.stop_times.trip.pattern.route.mode as route_mode,
    unnested_stops.stop_times.trip.pattern.route.color as route_color,
    unnested_stops.stop_times.trip.pattern.route.agency.name as agency_name,
    unnested_stops.stop_times.trip.pattern.route.agency.id as agency_id
from unnested_stops
