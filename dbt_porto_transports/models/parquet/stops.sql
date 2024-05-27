{{
    config(
        materialized='table'
    )
}}
select unnest(data.stops)
from {{ ref("stops_raw") }}
