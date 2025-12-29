import os
import time
import signal
import threading
from ingestion.runner import run_etl

INTERVAL = int(os.getenv("ETL_INTERVAL", "60"))


stop_event = threading.Event()


def _handle_signal(signum, frame):
    stop_event.set()


signal.signal(signal.SIGINT, _handle_signal)
signal.signal(signal.SIGTERM, _handle_signal)


def main():
    while not stop_event.is_set():
        try:
            run_etl()
        except Exception as exc:
            # keep worker alive on failure; metrics and logs should capture failures
            print("ETL run failed:", exc)
        # wait with early exit
        stop_event.wait(INTERVAL)


if __name__ == "__main__":
    main()
