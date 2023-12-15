## Trip delays

Another thing we can detect is how much time a bus is delayed. We can do this by comparing the scheduled time with the realtime time. We can do this by using the following query:


```sql last_times
select
  * exclude (rn)
from last_times
limit 100
```

The last_times provides uses the created_at to select the latest view befor the bus disappears and considers the delay as the final one.

With this we get the following table with the top delays per stop:

## Delays per stop

```sql top_delays_per_stop

from last_times
join stops using (stopId)
select stops.name as name, stops.lat as lat, stops.lon as lon, stops.route_shortName || ' - ' || stops.route_longName as routeName,
avg(last_times.arrivaldelay) as avg_delay_minutes
group by all
order by avg_delay_minutes desc
limit 100
```

<LeafletMap
data={top_delays_per_stop}
lat=lat
long=lon
name=name
tooltipFields={[ 'routeName', 'avg_delay_minutes']}
height=500
/>


```sql times_703
select * from last_times 
where route_shortName = '703'
and created_at < '2023-12-04'
and trip_id = 'VHJpcDoyOjcwM18wX0RfMTI='
order by created_at asc
```

## Delays per line

```sql top_delays_per_line

from last_times
join stops using (stopId)
select 
  stops.route_shortName || ' - ' || stops.route_longName as routeName,
first(stops.lat) as lat, 
first(stops.lon) as lon, 
avg(last_times.arrivaldelay) as avg_delay_minutes
group by all
having avg_delay_minutes > 5
order by avg_delay_minutes desc
limit 100
```

<LeafletMap
data={top_delays_per_line}
lat=lat
long=lon
name=routeName
tooltipFields={['avg_delay_minutes']}
height=500
/>

And what are the top 10 lines with less delays?

```sql bottom_delays_per_line

from last_times
join stops using (stopId)
select 
  stops.route_shortName || ' - ' || stops.route_longName as routeName,
first(stops.lat) as lat, 
first(stops.lon) as lon, 
avg(last_times.arrivaldelay) as avg_delay_minutes
group by all
having avg_delay_minutes < 100
order by avg_delay_minutes asc
limit 10
```

<LeafletMap
data={bottom_delays_per_line}
lat=lat
long=lon
name=routeName
tooltipFields={['avg_delay_minutes']}
height=500
/>

TODO: Average delays each day (all and per line)
