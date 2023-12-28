---
title: Info about bus and metro stops
---

Go to settings and point to the analysis.duckdb

## DuckDB tables

```sql tables
show tables
```

## Stops

```sql total_stops
select
  count(distinct stopId) as total
from stops
limit 1
```

<BigValue data={total_stops} value=total/>


```sql stops
select
  name, lat, lon, zoneId, route_shortName, route_longName
from stops
limit 100
```

<LeafletMap
data={stops}
lat=lat
long=lon
name=name
tooltipFields={['zoneId', 'route_shortName', 'route_longName']}
height=500
/>


## Total trips

```sql total_trips
select
  count(*) as total
from trip_stops
limit 1
```

<BigValue data={total_trips} value=total/>