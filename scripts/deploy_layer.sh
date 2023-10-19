#!/bin/bash

cd loader || exit
rm -rf python
poetry export --format=requirements.txt --output=requirements.txt --without-hashes
pip install -r requirements.txt -t python
rm -rf python/*dist-info
zip -r9 ../loader-layer.zip . -x "file_data/*" -x '*.pyc'
aws s3 mv ../loader-layer.zip s3://porto-realtime-transport/  

aws lambda publish-layer-version --layer-name porto-py-loader --content S3Bucket=porto-realtime-transport,S3Key=loader-layer.zip --compatible-runtimes python3.10,python3.11