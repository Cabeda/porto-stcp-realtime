{{
  config(
    materialized='table'
  )  
}}

select *
from 's3://porto-realtime-transport/file_data/2023/12/**/*.parquet'