{{
    config(
        materialized='table'
    )
}}
select
    stopId,
    ROUTE_SHORTNAME,
    ROUTE_LONGNAME,
    TRIP_ID,
    max(REALTIME) as realtime,
    epoch_ms(1000 * SERVICEDAY) as SERVICEDAY,
    min(epoch_ms(1000 * (SCHEDULEDDEPARTURE)))
from {{ref("trip_stops")}}
where realtime is true
group by all