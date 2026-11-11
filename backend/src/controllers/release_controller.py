from src.services.release_service import publish
from src.utils.serializers import serialize
from src.utils.audit import record

def create(db,data,user):
    row=publish(db,data,user); record(db,user,'publish_forecast',row.run_id); db.commit()
    return serialize(row)
