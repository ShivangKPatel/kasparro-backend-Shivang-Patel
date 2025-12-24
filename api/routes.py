from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from core.database import SessionLocal
from models.tables import Coin

router = APIRouter()

@router.get("/data")
def get_data(limit: int = 10, offset: int = 0):
    db = SessionLocal()
    data = db.query(Coin).offset(offset).limit(limit).all()
    return {"count": len(data), "data": data}

@router.get("/stats")
def stats():
    db = SessionLocal()
    return {"total_records": db.query(Coin).count()}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
