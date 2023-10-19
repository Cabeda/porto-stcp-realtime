#!/bin/bash

cd loader || exit
poetry export --format=requirements.txt --output=requirements.txt --without-hashes
rm -rf python
pip install -r requirements.txt -t python
zip -r9 ../loader.zip . -x "file_data/*" -x "python/*"

aws s3 mv ../loader.zip s3://porto-realtime-transport/  
aws lambda update-function-code --function-name explore-porto-to-parquet --s3-bucket porto-realtime-transport --s3-key loader.zip