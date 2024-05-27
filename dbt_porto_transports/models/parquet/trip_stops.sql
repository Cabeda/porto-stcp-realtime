{{
    config(
        materialized='table'
    )
}}

with unnested_stops as (
    /* select
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
        created_at,
        UNNEST(_stoptimeswithoutpatterns24f6pa) as stop_times
    {# from {{ref('trip_stops_raw')}} #}
    from {{ ref('december') }}
    union all */
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
        created_at,
        UNNEST(_stoptimeswithoutpatterns24f6pa) as stop_times
    {# from {{ref('trip_stops_raw')}} #}
    from {{ ref('may') }}
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
    unnested_stops.created_at,
    unnested_stops.stop_times.stop.id as stopid,
    unnested_stops.stop_times.serviceday as serviceday,
    unnested_stops.stop_times.realtimestate as realtimestate,
    unnested_stops.stop_times.realtimedeparture as realtimedeparture,
    unnested_stops.stop_times.scheduleddeparture as scheduleddeparture,
    unnested_stops.stop_times.realtimearrival as realtimearrival,
    unnested_stops.stop_times.scheduledarrival as scheduledarrival,
    unnested_stops.stop_times.arrivaldelay as arrivaldelay,
    unnested_stops.stop_times.departuredelay as departuredelay,
    unnested_stops.stop_times.realtime as realtime,
    unnested_stops.stop_times.pickuptype as pickuptype,
    unnested_stops.stop_times.headsign as headsign,
    unnested_stops.stop_times.trip.id as trip_id,
    unnested_stops.stop_times.trip.gtfsid as trip_gtfsid,
    unnested_stops.stop_times.trip.directionid as trip_directionid,
    unnested_stops.stop_times.trip.tripheadsign as trip_tripheadsign,
    unnested_stops.stop_times.trip.pattern.route.id as route_id,
    unnested_stops.stop_times.trip.pattern.route.gtfsid as route_gtfsid,
    unnested_stops.stop_times.trip.pattern.route.shortname as route_shortname,
    unnested_stops.stop_times.trip.pattern.route.longname as route_longname,
    unnested_stops.stop_times.trip.pattern.route.mode as route_mode,
    unnested_stops.stop_times.trip.pattern.route.color as route_color,
    unnested_stops.stop_times.trip.pattern.route.agency.name as agency_name,
    unnested_stops.stop_times.trip.pattern.route.agency.id as agency_id
from unnested_stops
