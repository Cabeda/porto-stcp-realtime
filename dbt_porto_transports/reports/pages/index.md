---
title: Info about bus and metro stops
---

Go to settings and point to the anaylsis.duckdb

## Stops

```sql stops
select
  name, lat, lon, zoneId, route_shortName, route_longName
from stops
limit 500
```

<LeafletMap
data={stops}
lat=lat
long=lon
name=name
tooltipFields={['zoneId', 'route_shortName', 'route_longName']}
height=500
/>

```sql total_stops
select
  count() as total
from stops
```

<BigValue data={total_stops} value=total/>
