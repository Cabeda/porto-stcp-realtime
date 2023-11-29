---
title: Delays of buses per stop
---

This demo [connects](/settings) to a local DuckDB file `analysis.duckdb`.

## Stops

```sql stops
select
  *
from stops
limit 10
```

```sql total_stops
select
  count() as total
from stops
```

<BigValue data={total_stops} value=total/>

## Trips

```sql trip_stops
select *
from trip_stops
limit 100
```


## Stops average cancelations

```sql stops_cancelations
select route_shortName || ' - ' || route_longName as routeName, ratio, *
from canceled_trips_agg
where route_longName != '-'
order by ratio asc
```
