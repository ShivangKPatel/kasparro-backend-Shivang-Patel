from fastapi import APIRouter, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from core.database import SessionLocal
from models.tables import Coin

router = APIRouter()


def _coin_to_dict(c: Coin) -> dict:
    # Convert SQLAlchemy Coin model to JSON-serializable dict
    return {
        "id": c.id,
        "canonical_id": getattr(c, "canonical_id", None),
        "symbol": c.symbol,
        "name": c.name,
        "price_usd": float(c.price_usd) if c.price_usd is not None else None,
        "market_cap_usd": float(c.market_cap_usd) if c.market_cap_usd is not None else None,
        "volume_24h_usd": float(c.volume_24h_usd) if c.volume_24h_usd is not None else None,
        "source": c.source,
        "last_updated": c.last_updated.isoformat() if c.last_updated else None,
    }


@router.get("/data")
def get_data(limit: int = 10, offset: int = 0):
    db = SessionLocal()
    data = db.query(Coin).offset(offset).limit(limit).all()
    return {"count": len(data), "data": [_coin_to_dict(c) for c in data]}


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
