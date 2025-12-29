import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    # Use container-internal Postgres port 5432 by default when running with docker-compose
    "postgresql+psycopg2://postgres:postgres@db:5432/kasparro"
)

FAIL_AFTER_N_RECORDS = int(os.getenv("FAIL_AFTER_N_RECORDS", "0"))