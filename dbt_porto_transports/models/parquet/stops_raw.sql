{{
    config(
        materialized='table'
    )
}}
select * 
from 'data/stops.json'