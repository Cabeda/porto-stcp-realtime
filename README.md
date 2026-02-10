# porto-stcp-realtime

Collects real-time STCP bus data from Porto, Portugal and analyzes it against the provided schedule. Data is fetched from the [explore.porto.pt](https://explore.porto.pt/) GraphQL API every minute.

## Architecture

```
explore.porto.pt GraphQL API
        │
        ├──► Python Loader (AWS Lambda) ──► Parquet ──► S3
        │                                                │
        │                                                ▼
        │                                     dbt (DuckDB) ──► Evidence Reports
        │
        └──► Deno Loader (alternative) ──► SQLite (local/K8s)
```

## Components

### Python Loader (`loader/`)

AWS Lambda function (Python 3.11) that fetches real-time stop data and writes Parquet files to S3.

- Runs every minute via CloudWatch scheduled event
- Writes to `s3://porto-realtime-transport/file_data/{year}/{month}/{day}/{epoch}.parquet`
- Error notifications via SNS
- Dependencies: pandas, pyarrow, boto3 (via AWS SDK Pandas Lambda layer)

```shell
cd loader
poetry install
poetry run python3 main.py  # runs locally in a loop
```

**Deploy** (via Serverless Framework):

```shell
cd loader
npx serverless deploy
```

CI/CD: Automatically deployed on push to `main` via GitHub Actions.

### Deno Loader (`deno_loader/`)

Alternative loader that stores data in a local SQLite database. Deployable via Docker/Kubernetes.

```shell
cd deno_loader
deno run --allow-read --allow-net --allow-write main.ts
```

**Docker:**

```shell
docker build -t porto-stcp .
docker run porto-stcp
```

**Kubernetes:** See `deployment.yml` for K8s manifest.

### dbt Project (`dbt_porto_transports/`)

Data transformation and analysis using [dbt](https://docs.getdbt.com/) with the [dbt-duckdb](https://github.com/jwills/dbt-duckdb) adapter. Reads Parquet files from S3 and produces analytical models (trip stops, cancellations, aggregations).

```shell
cd dbt_porto_transports
poetry install
poetry run dbt run
```

**Reports** (`dbt_porto_transports/reports/`): Built with [Evidence](https://evidence.dev/) for data visualization.

```shell
cd dbt_porto_transports/reports
npm install
npm run dev
```

## Infrastructure

| Resource | Details |
|---|---|
| AWS Region | `eu-central-1` |
| S3 Bucket | `porto-realtime-transport` |
| Lambda Runtime | Python 3.11 (arm64) |
| Lambda Layer | AWS SDK Pandas (arm64) |
| SNS Topic | Error notifications |
| CI/CD | GitHub Actions → Serverless Framework |

## Data Source

GraphQL endpoint: `https://otp.services.porto.digital/otp/routers/default/index/graphql`

Fetches all stops with up to 5 upcoming departures within a 12-hour window, including real-time vs scheduled arrival/departure times, delays, route info, and agency data.
