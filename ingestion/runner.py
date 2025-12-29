import time
from core.database import SessionLocal
from core.metrics import ETL_RUNS_TOTAL, ETL_FAILURES_TOTAL
from core.config import FAIL_AFTER_N_RECORDS
from ingestion.coinpaprika_source import fetch_coinpaprika
from ingestion.coingecko_source import fetch_coingecko
from ingestion.transformer import normalize_coin
from models.tables import RawData, Coin, Checkpoint

def run_etl():
    db = SessionLocal()
    ETL_RUNS_TOTAL.inc()
    processed = 0

    try:
        sources = {
            "coinpaprika": fetch_coinpaprika(),
            "coingecko": fetch_coingecko()
        }

        for source, records in sources.items():
            cp = db.query(Checkpoint).filter_by(source=source).first()
            if cp is None:
                cp = Checkpoint(source=source, cursor="0")
                db.add(cp)

            for idx, r in enumerate(records):
                if idx <= int(cp.cursor):
                    continue

                processed += 1
                if FAIL_AFTER_N_RECORDS and processed >= FAIL_AFTER_N_RECORDS:
                    raise RuntimeError("Injected failure")

                db.add(RawData(source=source, payload=r))
                # Normalize and upsert by canonical_id to unify identities across sources
                coin_data = normalize_coin(r, source)
                canonical = coin_data.get("canonical_id")
                if canonical:
                    existing = db.query(Coin).filter_by(canonical_id=canonical).first()
                    if existing:
                        # update numeric fields and last_updated/source
                        existing.price_usd = coin_data.get("price_usd")
                        existing.market_cap_usd = coin_data.get("market_cap_usd")
                        existing.volume_24h_usd = coin_data.get("volume_24h_usd")
                        existing.last_updated = coin_data.get("last_updated")
                        existing.source = coin_data.get("source")
                    else:
                        db.add(Coin(**coin_data))
                else:
                    db.add(Coin(**coin_data))
                cp.cursor = str(idx)

            db.commit()

    except Exception:
        db.rollback()
        ETL_FAILURES_TOTAL.inc()
        raise
    finally:
        db.close()
