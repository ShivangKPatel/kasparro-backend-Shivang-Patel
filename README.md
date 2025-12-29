# Kasparro ETL

Production-ready ETL pipeline for cryptocurrency data aggregation from multiple sources (CoinGecko, CoinPaprika) with identity unification.

## Features

- **Multi-source ingestion**: CoinGecko and CoinPaprika APIs
- **Identity unification**: Canonical ID mapping across sources (`symbol:name`)
- **Resilient ETL**: Exponential backoff, rate limiting, checkpoint-based recovery
- **Multi-stage Docker**: Optimized slim images with non-root user
- **Observability**: Prometheus metrics, structured logging, health endpoints
- **API**: FastAPI with `/data`, `/stats`, `/health`, `/metrics` endpoints

## Quick Start

### Local Development

```bash
cd kasparro-etl
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### Docker Compose (Recommended)

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials

# Build and run all services
docker-compose up --build

# Run only API
docker-compose up --build app

# Run only ETL worker
docker-compose up --build worker
```

## Configuration

Create a `.env` file (do **not** commit secrets). See `.env.example`:

```env
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-secure-password>
POSTGRES_DB=kasparro
DATABASE_URL=postgresql+psycopg2://postgres:<password>@db:5432/kasparro

# Application
APP_ENV=production
LOG_LEVEL=INFO
ETL_INTERVAL=60
PYTHONUNBUFFERED=1
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  CoinGecko  │     │ CoinPaprika │     │  (Future)   │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────┬───────┴───────────────────┘
                   ▼
         ┌─────────────────┐
         │   ETL Worker    │  (ingestion/worker.py)
         │  - Rate limit   │
         │  - Backoff      │
         │  - Normalize    │
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │  Identity Unify │  (canonical_id = symbol:name)
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │   PostgreSQL    │
         │  - coins        │
         │  - raw_data     │
         │  - checkpoints  │
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │   FastAPI App   │  (api/main.py)
         │  GET /data      │
         │  GET /stats     │
         │  GET /health    │
         │  GET /metrics   │
         └─────────────────┘
```

## Cloud Deployment

> **Note on cloud credentials**
>
> The following subsections describe how this project *could* be deployed to common cloud platforms (AWS, Azure, GCP) using the existing Docker setup. At the moment, there are no active cloud credits or accounts available for this project (previous student/free-tier credits for AWS and GCP have expired), so there is **no live cloud deployment** running. You can still run everything locally via Docker Compose or directly with Python as described above.

### AWS ECS / Fargate

1. Push Docker image to ECR:
   ```bash
   aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
   docker build -t kasparro-etl .
   docker tag kasparro-etl:latest <account>.dkr.ecr.<region>.amazonaws.com/kasparro-etl:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/kasparro-etl:latest
   ```

2. Create ECS task definitions for `app` and `worker` services
3. Use RDS PostgreSQL for managed database
4. Configure secrets via AWS Secrets Manager

### Azure Container Apps

1. Push to Azure Container Registry:
   ```bash
   az acr login --name <registry>
   docker build -t <registry>.azurecr.io/kasparro-etl:latest .
   docker push <registry>.azurecr.io/kasparro-etl:latest
   ```

2. Deploy Container App with managed identity
3. Use Azure Database for PostgreSQL
4. Store secrets in Azure Key Vault

### Google Cloud Run

1. Push to Artifact Registry:
   ```bash
   gcloud auth configure-docker <region>-docker.pkg.dev
   docker build -t <region>-docker.pkg.dev/<project>/kasparro/etl:latest .
   docker push <region>-docker.pkg.dev/<project>/kasparro/etl:latest
   ```

2. Deploy to Cloud Run
3. Use Cloud SQL for PostgreSQL
4. Configure secrets via Secret Manager

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Liveness probe |
| `/data` | GET | Paginated coin data (`?limit=10&offset=0`) |
| `/stats` | GET | Database statistics |
| `/metrics` | GET | Prometheus metrics |

## Testing

```bash
pytest -v
```

## License

MIT
