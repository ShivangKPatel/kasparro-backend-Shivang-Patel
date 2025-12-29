from fastapi import FastAPI
from api.routes import router
from core.database import engine
from models.tables import Base

app = FastAPI()


@app.on_event("startup")
def on_startup():
	# Ensure tables exist. Do NOT run ETL inside the web process — use the separate worker.
	Base.metadata.create_all(engine)


app.include_router(router)
