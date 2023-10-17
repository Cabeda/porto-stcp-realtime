import json
import time

import boto3
import pandas as pd
import pyarrow.parquet as pq
import requests
from pyarrow import Table


def get_stop_realtime(date: int) -> Table:
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

    response = requests.post(
        "https://otp.services.porto.digital/otp/routers/default/index/graphql",
        headers=headers,
        data=json.dumps(bodyQL),
    )

    if response.status_code == 200:
        json_data = response.json()
        if "errors" in json_data:
            print(json_data["errors"])
            return None
        return json_data["data"]["stops"]
    else:
        print(f"Error: {response.status_code}")
        return None

def write_to_json(data, filename: str):
    with open(filename, 'w') as f:
        json.dump(data, f)

def write_to_parquet(df: Table, filename: str):
    print(f"Writing {filename}")
    pq.write_table(df, filename)

def write_to_s3(s3Client, filename):
    # Upload the Parquet file to S3
    print(f"Uploading {filename} to S3")
    bucket_name = 'porto-realtime-transport'
    s3Client.upload_file(filename, bucket_name, filename)
    # Delete the local Parquet file
    #os.remove(filename)

if __name__ == "__main__":
    session = boto3.Session(profile_name='personal')
    s3 = session.client('s3')
    
    while True:
        
      date = int(time.time())
      filename = f"file_data/{date}"
      

      response = get_stop_realtime(date)
      df = pd.DataFrame(response)
      table = Table.from_pandas(df)
      write_to_parquet(table, f"{filename}.parquet")
      write_to_s3(s3, f"{filename}.parquet")

      print("Sleeping for 60 seconds")
      time.sleep(60)
  
  
    

        