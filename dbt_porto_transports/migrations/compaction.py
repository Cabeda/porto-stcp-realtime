from datetime import datetime, timedelta

import duckdb

start_date = datetime(2024, 2, 1)
end_date = datetime(2024, 5, 15)
delta = timedelta(days=1)

with duckdb.connect() as con:
    while start_date <= end_date:
        year = start_date.strftime("%Y")
        month = start_date.strftime("%-m")
        day = start_date.strftime("%-d")

        print(start_date.strftime("%Y%m%d"))
        try:
            con.execute(f"copy (from 's3://porto-realtime-transport/file_data/{year}/{month}/{day}/*.parquet') to 's3://porto-realtime-transport/file_data/{year}/{month}/{year}{month}{day}.parquet' (compression ZSTD)")
        except Exception as e:
            print(e)
            # Append to log file
            with open("log.txt", "a") as file:
                file.write(f"Error: {e} on {start_date.strftime('%Y%m%d')}\n")


        start_date += delta
