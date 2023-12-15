{{
  config(
    materialized='table'
  )  
}}

select *
from 's3://porto-realtime-transport/file_data/**/*.parquet'

-- TODO: clean files throwing error on import