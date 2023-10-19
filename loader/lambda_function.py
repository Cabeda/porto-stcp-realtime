import json
import pathlib
import time
import urllib.request

import boto3
import polars as pl


def get_stop_realtime(date: int) -> json:
    query = """
    query StopRoute(
      $startTime_1: Long!
      $timeRange_2: Int!
      $numberOfDepartures_3: Int!
    ) {
      stops {
        id
        name
        code
        lat
        lon
        locationType
        zoneId
        vehicleType
        vehicleMode
        platformCode
        ...F3
      }
    }
    fragment F1 on Stoptime {
      serviceDay
      realtimeState
      realtimeDeparture
      scheduledDeparture
      realtimeArrival
      scheduledArrival
      arrivalDelay 
      departureDelay
      realtime
      serviceDay
      pickupType
      headsign
      
      stop {
        id
        code
        platformCode
      }
      trip {
        gtfsId
        directionId
        tripHeadsign
        pattern {
          route {
            gtfsId
            shortName
            longName
            mode
            color
            agency {
              name
              id
            }
            id
          }
          code
          id
        }
        id
      }
    }
    
    fragment F2 on Stop {
      gtfsId
      name
      desc
      zoneId
      id
    }
    fragment F3 on Stop {
      gtfsId
      _stoptimesWithoutPatterns24f6Pa: stoptimesWithoutPatterns(
        startTime: $startTime_1
        timeRange: $timeRange_2
        numberOfDepartures: $numberOfDepartures_3
        omitCanceled: true
      ) {
        ...F1
      }
      id
      ...F2
    }
    """

    bodyQL = {
        "query": query,
        "operationName": "StopRoute",
        "variables": {
            "startTime_1": date,  # Epoch time in seconds
            "timeRange_2": 43200,
            "numberOfDepartures_3": 5,
        },
    }

    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://explore.porto.pt/",
        "OTPTimeout": "10000",
        "Origin": "https://explore.porto.pt",
        "DNT": "1",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    print(f"Fetching data for period {date}")

    req = urllib.request.Request(
        url="https://otp.services.porto.digital/otp/routers/default/index/graphql",
        headers=headers,
        data=json.dumps(bodyQL).encode("utf-8"),
        method="POST",
    )

    with urllib.request.urlopen(req) as response:
        if response.status == 200:
            json_data = json.loads(response.read().decode("utf-8"))
            if "errors" in json_data:
                print(json_data["errors"])
                return None
            return json_data["data"]["stops"]
        else:
            print(f"Error: {response.status}")
            return None


def write_to_json(data, filename: str):
    with open(filename, "w") as f:
        json.dump(data, f)


def write_to_parquet(df, filename: pathlib.Path):
    print(f"Writing {filename}")
    # pq.write_table(df, filename)
    pathlib.Path("file_data").mkdir(parents=True, exist_ok=True)
    df.write_parquet(filename)


def write_to_s3(s3Client, filename):
    # Upload the Parquet file to S3
    print(f"Uploading {filename} to S3")
    bucket_name = "porto-realtime-transport"
    s3Client.upload_file(filename, bucket_name, filename)
    # Delete the local Parquet file
    # os.remove(filename)


def lambda_handler(event, context):
    session = boto3.Session()
    s3 = session.client("s3")

    date = int(time.time())
    filename = f"file_data/{date}"
    path: pathlib.Path = pathlib.Path(f"file_data/{date}.parquet")

    response = get_stop_realtime(date)
    df = pl.DataFrame(response)

    # table = Table.from_pandas(df)
    write_to_parquet(df, path)
    write_to_s3(s3, f"{filename}.parquet")


if __name__ == "__main__":
    while True:

        lambda_handler({}, None)
        print("Sleeping for 60 seconds")
        time.sleep(60)
