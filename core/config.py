import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5435/kasparro"
)

FAIL_AFTER_N_RECORDS = int(os.getenv("FAIL_AFTER_N_RECORDS", "0"))