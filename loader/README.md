# Loader

Executes request to explore.porto.pt and writes to S3 bucket in parquet files.

## Requirements

Generate using the command:

```python
poetry export --format=requirements.txt --output=requirements.txt --without-hashes
```

## Generate zip for AWS Lambda

```bash
cd loader
poetry export --format=requirements.txt --output=requirements.txt --without-hashes
pip install -r requirements.txt -t .
zip -r9 ../loader.zip . -x "file_data/*"
```

## Generate zip loader for AWS Lambda

```bash
cd loader
poetry export --format=requirements.txt --output=requirements.txt --without-hashes
pip install -r requirements.txt -t python
zip -r9 ../loader-layer.zip . -x "file_data/*"
aws s3 mv ../loader-layer.zip s3://porto-realtime-transport/
```

## Deploy to AWS Lambda

```bash
aws s3 mv ../loader.zip s3://porto-realtime-transport/
aws lambda update-function-code --function-name explore-porto-to-parquet --s3-bucket porto-realtime-transport --s3-key loader.zip --profile personal

```

## Call AWS Lambda

```bash
aws lambda invoke --function-name explore-porto-to-parquet --payload '{}' --profile personal outputfile.txt
```
