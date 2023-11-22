{{
  config(
    materialized='table'
  )  
}}


SELECT *
FROM
    iceberg_scan('s3://porto-realtime-transport/iceberg/stops_raw_iceberg/metadata/00000-02fa2214-1530-4337-91b5-ae429ae23e44.metadata.json')
