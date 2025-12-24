from fastapi import FastAPI
from api.routes import router
from core.database import engine
from models.tables import Base
from ingestion.runner import run_etl

Base.metadata.create_all(engine)
run_etl()

app = FastAPI()
app.include_router(router)
