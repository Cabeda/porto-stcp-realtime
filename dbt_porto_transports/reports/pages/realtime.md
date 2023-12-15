# Realtime

Can we get the latest data directly? If we query the files directly.

```sql realtime
call load_aws_credentials("personal");

select count()
from 's3://porto-realtime-transport/file_data/2023/12/8/170203*.parquet'
```