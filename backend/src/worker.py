import time,logging
from pathlib import Path
from src.config.database import SessionLocal
from src.config.queue import queue,QUEUE_NAME
from src.models import ForecastRun
from src.services.run_service import compute
logging.basicConfig(level=logging.INFO)
while True:
    Path('/tmp/heartbeat').touch()
    try:
        item=queue.blpop(QUEUE_NAME,timeout=4)
        if not item: continue
        run_id=int(item[1])
        with SessionLocal() as db:
            try: compute(db,run_id)
            except Exception as exc:
                db.rollback()
                run=db.get(ForecastRun,run_id)
                if run:
                    run.status='failed'; run.error=str(exc)[:500]; db.commit()
                logging.exception('forecast %s failed',run_id)
    except Exception:
        logging.exception('worker loop failed'); time.sleep(2)
