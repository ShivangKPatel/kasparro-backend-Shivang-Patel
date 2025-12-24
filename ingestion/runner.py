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
            cp = db.get(Checkpoint, source) or Checkpoint(source=source, cursor="0")
            db.add(cp)

            for idx, r in enumerate(records):
                if idx <= int(cp.cursor):
                    continue

                processed += 1
                if FAIL_AFTER_N_RECORDS and processed >= FAIL_AFTER_N_RECORDS:
                    raise RuntimeError("Injected failure")

                db.add(RawData(source=source, payload=r))
                db.add(Coin(**normalize_coin(r, source)))
                cp.cursor = str(idx)

            db.commit()

    except Exception:
        db.rollback()
        ETL_FAILURES_TOTAL.inc()
        raise
    finally:
        db.close()
