# Realtime

Can we get the latest data directly? If we query the files directly.

```sql realtime
call load_aws_credentials("default");
set s3_region='eu-central-1';

select count()
from 's3://porto-realtime-transport/file_data/2024/1/6/*.parquet'
```