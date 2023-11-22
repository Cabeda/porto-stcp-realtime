-- Create athena results bucket
-- Create glue db to store metadata loc s3://porto-realtime-transport/glue_metadata/

CREATE TABLE porto.stops_raw_iceberg (
  id string, 
  name string, 
  code string, 
  lat string, 
  lon string, 
  locationtype string, 
  zoneid string, 
  vehicletype bigint, 
  vehiclemode string, 
  platformcode int, 
  gtfsid string, 
  _stoptimeswithoutpatterns24f6pa array<struct<arrivalDelay:bigint,departureDelay:bigint,headsign:string,pickupType:string,realtime:boolean,realtimeArrival:bigint,realtimeDeparture:bigint,realtimeState:string,scheduledArrival:bigint,scheduledDeparture:bigint,serviceDay:bigint,stop:struct<code:string,id:string,platformCode:int>,trip:struct<directionId:string,gtfsId:string,id:string,pattern:struct<code:string,id:string,route:struct<agency:struct<id:string,name:string>,color:string,gtfsId:string,id:string,longName:string,mode:string,shortName:string>>,tripHeadsign:string>>>, 
  desc int, 
  created_at timestamp
)
PARTITIONED BY (code, bucket(16, id))
LOCATION 's3://porto-realtime-transport/iceberg/trip_stops_iceberg/'
TBLPROPERTIES (
    'table_type' = 'ICEBERG',
    'format'='parquet'
);

