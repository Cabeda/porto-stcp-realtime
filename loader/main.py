import datetime
import json
import logging
import pathlib
import time
import urllib.request

import boto3
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.ERROR)

sns_client = boto3.client('sns')
topic_arn = 'arn:aws:sns:eu-central-1:380030078937:porto-realtime-errors'


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
    df.to_parquet(filename)


def write_to_s3(s3Client, file_path, filename):
    # Upload the Parquet file to S3
    print(f"Uploading {filename} to S3")
    bucket_name = "porto-realtime-transport"
    s3Client.upload_file(file_path, bucket_name, filename)


def handler(event, context):
    try:
      session = boto3.Session()
      s3 = session.client("s3")

      date = int(time.time())
      filename = f"{date}.parquet"
      year = datetime.datetime.now().year
      month = datetime.datetime.now().month
      day = datetime.datetime.now().day
      print(f"Year: {year}, Month: {month}, Day: {day}")
      path: pathlib.Path = pathlib.Path(f"/tmp/{filename}")
      print(f"file_data/{year}/{month}/{day}/{filename}")
      response = get_stop_realtime(date)
      df = pd.DataFrame(response)

      write_to_parquet(df, path)
      write_to_s3(s3, path, f"file_data/{year}/{month}/{day}/{filename}")
      return {
      'statusCode': 200,
      'body': f"Written {filename} to S3 with success!"
    }
    except Exception as e:
      logger.error(e)
      sns_client.publish(
            TopicArn=topic_arn,
            Subject='Porto realtime function error',
            Message=str(e)
        )
      raise e


if __name__ == "__main__":
    while True:

        handler({}, None)
        print("Sleeping for 60 seconds")
        time.sleep(60)
