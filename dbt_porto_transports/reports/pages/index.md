---
title: Info about bus and metro stops
---

Go to settings and point to the analysis.duckdb

## DuckDB tables

```sql tables
select * from analysis.tables
```

## Stops

```sql total_stops
select
  count(distinct stopId) as total
from analysis.stops
limit 1
```

<BigValue data={total_stops} value=total/>


```sql stops
select
  name, lat, lon, zoneId, route_shortName, route_longName
from analysis.stops
limit 100
```

<!-- <LeafletMap
data={stops}
lat=lat
long=lon
name=name
tooltipFields={['zoneId', 'route_shortName', 'route_longName']}
height=500
/> -->


## Total trips

```sql total_trips
select
  count(*) as total
from analysis.trip_stops
limit 1
```

<BigValue data={total_trips} value=total/>