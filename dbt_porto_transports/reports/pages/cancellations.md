## Trip cancelations

So we have the 5 next trips every minute for every top.

```sql trip_stops
select *
from trip_stops
limit 100
```

How can we detect that a trip was canceled (no bus will appear)? After doing some field inpection I've found that when there's no real time signal for the entire trip the bus just wouldn't appear. We can check the realtime field for that.

```sql realtime_field_trip

select
  case when realtime is true then 'Realtime' else 'Scheduled' end as name,
  count() as value
from trip_stops
group by 1
```

<ECharts config={
{
legend: {
top: 'bottom'
},
tooltip: {
formatter: '{b}: {c} ({d}%)',
trigger: 'item'
},
series: [
{
type: 'pie',
data: realtime_field_trip,
}
]
}
}
/>

From the chart above, we can see that most of the results are only scheduled. We can't yet take any conclusions as we don't know how reliable the gps signal is. So we keep with the definition of canceled as:

> All the trips that have no realtime signal for the entire trip.

With this definition, we have set a model to get this like shown on the following query:

```sql canceled_trips

select
  *
  from canceled_trips
  limit 100
```

### Stops cancelations

```sql stops_cancelations
select stops.name, lat, lon, stops.route_shortName || ' - ' || stops.route_longName as routeName, ratio
from canceled_trips_agg
join stops using (stopId)
where stops.route_longName != '-'
order by ratio asc
limit 300
```


<LeafletMap
data={stops_cancelations}
lat=lat
long=lon
name=name
tooltipFields={[ 'routeName', 'ratio']}
height=500
/>

## Line cancelations

```sql line_cancelations
select stops.route_shortName || ' - ' || stops.route_longName as routeName, avg(ratio) as ratio, first(lon) as lon, first(lat) as lat
from canceled_trips_agg
join stops using (stopId)
where stops.route_longName != '-'
group by routeName, ratio
order by ratio asc
limit 10
```

<LeafletMap
data={line_cancelations}
lat=lat
long=lon
name=name
tooltipFields={[ 'routeName', 'ratio']}
height=500
width=1000
/>


TODO: Average cancellations each day (all and per line)