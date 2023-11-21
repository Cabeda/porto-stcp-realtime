with all_times as (
    from trip_stops
    select
        trip_gtfsid,
        trip_id,
        arrivaldelay,
        scheduledarrival,
        created_at,
        route_id,
        route_shortName,
        row_number() over (partition by trip_id, scheduledarrival order by arrivaldelay desc) as rn
)
select *
from all_times
where rn = 1