create or replace table stops as SELECT * FROM sqlite_scan('stcp.db', 'stop_realtime');

create table stops_raw as select * from 'stops.json';
create table routes_raw as select * from 'routes.json';