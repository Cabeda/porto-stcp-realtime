# AGENTS.md

Guidance for AI coding agents working on this project.

## Project Overview

Real-time STCP (Porto, Portugal) bus data collection and analysis pipeline. Fetches stop/departure data from a GraphQL API every minute, stores it, and transforms it with dbt for analysis.

## Repository Structure

```
├── loader/              # Python AWS Lambda loader (primary)
├── deno_loader/         # Deno/TypeScript alternative loader
├── dbt_porto_transports/  # dbt project for data transformation
│   ├── models/parquet/  # Main dbt models (DuckDB over S3 Parquet)
│   ├── models/sqlite/   # Models for SQLite source
│   ├── models/iceberg/  # Models for Iceberg format
│   ├── reports/         # Evidence.dev reporting app
│   ├── data/            # Static reference data (stops.json, routes.json)
│   ├── migrations/      # Data migration scripts
│   └── scripts/         # Utility scripts (e.g., S3 file moves)
├── scripts/             # Lambda deployment shell scripts
├── presentation/        # Presentation materials
├── Dockerfile           # Deno loader container (Alpine + Deno 1.37)
├── deployment.yml       # Kubernetes manifest for Deno loader
└── .github/workflows/   # CI/CD (deploys Lambda on push to main)
```

## Component Details

### Python Loader (`loader/`)

- **Language**: Python 3.11
- **Package manager**: Poetry (`pyproject.toml`)
- **Entry point**: `main.py` — `handler(event, context)` for Lambda, `__main__` block for local loop
- **Dependencies**: pandas, pyarrow, boto3 (boto3 provided by Lambda layer at runtime, listed as dev dep)
- **Deployment**: Serverless Framework (`serverless.yml`) — `npx serverless deploy`
- **Lambda config**: arm64, 512MB memory, 20s timeout, scheduled every 1 minute
- **Data flow**: GraphQL API → pandas DataFrame → Parquet → S3 (`porto-realtime-transport/file_data/{year}/{month}/{day}/{epoch}.parquet`)
- **Error handling**: Catches exceptions, publishes to SNS topic, re-raises

### Deno Loader (`deno_loader/`)

- **Language**: TypeScript (Deno runtime)
- **Entry point**: `main.ts`
- **Types**: `types.ts` — `StopRealtime`, `Stop`, `StopTime`, `APIResponse`
- **Storage**: SQLite (creates `stcp_{epoch}.db` file)
- **Runs**: Fetches once, then `setInterval` every 60s
- **Container**: Dockerfile at repo root (Deno 1.37, Alpine-based)
- **Permissions needed**: `--allow-read --allow-net --allow-write`

### dbt Project (`dbt_porto_transports/`)

- **Language**: SQL (dbt)
- **Python**: 3.12 (separate from loader)
- **Package manager**: Poetry
- **Adapter**: dbt-duckdb 1.8.0, DuckDB 0.10
- **Profile**: `dbt_porto_transports` (configure in `~/.dbt/profiles.yml`)
- **Key models** (in `models/parquet/`):
  - `stops_raw`, `stops` — raw and cleaned stop data
  - `routes_raw` — route reference data
  - `trip_stops_raw`, `trip_stops` — departure/arrival data with delays
  - `canceled_trips`, `canceled_trips_agg`, `canceled_trips_daily_agg` — cancellation analysis
  - `last_times` — latest data timestamps
  - Month-specific models (`april`, `may`, `november`, `december`)
- **Reports**: Evidence.dev app in `reports/` — Node.js, run with `npm run dev`

## Data Source

- **API**: `https://otp.services.porto.digital/otp/routers/default/index/graphql`
- **Operation**: `StopRoute` query — fetches all stops with up to 5 departures in a 12-hour window
- **Key fields**: stop ID/name/lat/lon, scheduled vs realtime arrival/departure, delays, route/trip/agency info, `realtimeState` (e.g., `SCHEDULED`, `UPDATED`, `CANCELED`)
- **Auth**: None (public API, requires `Origin: https://explore.porto.pt` header)

## AWS Infrastructure

| Resource | Value |
|---|---|
| Region | `eu-central-1` |
| S3 Bucket | `porto-realtime-transport` |
| Lambda Function | `porto-realtime-loader` (via Serverless) |
| Lambda Layer | `AWSSDKPandas-Python311-Arm64` (AWS-managed) |
| SNS Topic | `porto-realtime-errors` |
| CI/CD | GitHub Actions → Serverless Framework |

## Development Commands

```shell
# Python loader
cd loader && poetry install && poetry run python3 main.py

# Deno loader
cd deno_loader && deno run --allow-read --allow-net --allow-write main.ts

# dbt
cd dbt_porto_transports && poetry install && poetry run dbt run

# Evidence reports
cd dbt_porto_transports/reports && npm install && npm run dev

# Deploy Lambda
cd loader && npx serverless deploy
```

## Conventions

- Python uses Poetry for dependency management (no pip requirements.txt committed)
- Deno imports from `https://deno.land/x/` URLs directly
- dbt models are SQL files; naming follows `{entity}` / `{entity}_raw` / `{entity}_agg` pattern
- Parquet files on S3 are partitioned by `year/month/day`
- No tests currently exist — add tests in `dbt_porto_transports/tests/` for dbt, or alongside source for Python/Deno
- `.gitignore` excludes: `*.db`, `*.duckdb`, `*.parquet`, `node_modules`, `__pycache__`, `.serverless`

## Common Pitfalls

- The GraphQL API requires specific headers (especially `Origin` and `Referer`) or requests will be rejected
- boto3 is a dev dependency in the loader because Lambda provides it via the AWS SDK Pandas layer at runtime
- The dbt project needs a `profiles.yml` configured with S3 access to read Parquet files
- DuckDB version must stay at 0.10.x to match dbt-duckdb 1.8.0 compatibility
