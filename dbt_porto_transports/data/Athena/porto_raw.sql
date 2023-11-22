CREATE EXTERNAL TABLE porto.porto_rawfile_data(
  id string, 
  name string, 
  code string, 
  lat double, 
  lon double, 
  locationtype string, 
  zoneid string, 
  vehicletype bigint, 
  vehiclemode string, 
  platformcode int, 
  gtfsid string, 
  _stoptimeswithoutpatterns24f6pa array<struct<arrivalDelay:bigint,departureDelay:bigint,headsign:string,pickupType:string,realtime:boolean,realtimeArrival:bigint,realtimeDeparture:bigint,realtimeState:string,scheduledArrival:bigint,scheduledDeparture:bigint,serviceDay:bigint,stop:struct<code:string,id:string,platformCode:int>,trip:struct<directionId:string,gtfsId:string,id:string,pattern:struct<code:string,id:string,route:struct<agency:struct<id:string,name:string>,color:string,gtfsId:string,id:string,longName:string,mode:string,shortName:string>>,tripHeadsign:string>>>, 
  desc int, 
  created_at timestamp)
PARTITIONED BY ( 
  partition_0 string, 
  partition_1 string, 
  partition_2 string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://porto-realtime-transport/file_data/'
TBLPROPERTIES (
  'classification'='parquet', 
  'compressionType'='none', 
  'partition_filtering.enabled'='true', 
  'typeOfData'='file')