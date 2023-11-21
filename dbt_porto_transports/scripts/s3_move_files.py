import datetime

import boto3

s3 = boto3.client("s3")
bucket_name = "porto-realtime-transport"
prefix = "file_data"

response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

for obj in response["Contents"]:
    if not obj["Key"].startswith("file_data/2023"):
        filename = obj["Key"].replace("file_data/", "")
        name = filename.replace(".parquet", "")
        date = datetime.datetime.fromtimestamp(int(name))
        year = date.year
        month = date.month
        day = date.day

        new_key = f"{prefix}/{year}/{month}/{day}/{filename}"
        copy_source = {
            'Bucket': bucket_name,
            'Key': obj["Key"]
        }
        print(f"Move s3://{bucket_name}/{prefix}/{filename} to {new_key}")

        s3.copy(copy_source, bucket_name, new_key)
        s3.delete_object(Bucket=bucket_name, Key=obj["Key"])

