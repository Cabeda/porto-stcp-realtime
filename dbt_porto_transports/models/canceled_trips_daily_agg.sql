select
    route_longName,
    route_shortName,
    serviceDay,
    count() filter (where realtime is true) as trip,
    count() filter (where realtime is false) as canceled,
    count() filter (where realtime is true) / count()::float as ratio
from canceled_trips
group by route_longName, route_shortName, serviceDay
order by ratio desc