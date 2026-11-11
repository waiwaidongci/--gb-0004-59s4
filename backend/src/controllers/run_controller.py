from src.services.run_service import create_run,enqueue
from src.utils.serializers import serialize
from src.utils.audit import record

def create(db,data,user):
    run=create_run(db,data,user)
    record(db,user,'create_forecast',run.name); db.commit()
    try: enqueue(run.id)
    except Exception:
        run.status='failed'; run.error='任务队列不可用，请重新创建'; db.commit()
    return serialize(run)
