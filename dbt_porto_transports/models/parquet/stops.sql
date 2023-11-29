select unnest(data.stops)
from {{ ref("stops_raw") }}
