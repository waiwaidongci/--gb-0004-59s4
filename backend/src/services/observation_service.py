from sqlalchemy import select
from fastapi import HTTPException
from src.models import Observation
from src.utils.serializers import serialize
from .series_service import get_series

def observations(db,series_id):
    get_series(db,series_id)
    return [serialize(o) for o in db.scalars(select(Observation).where(Observation.series_id==series_id).order_by(Observation.day))]

def add_observation(db,series_id,data):
    get_series(db,series_id)
    if db.scalar(select(Observation).where(Observation.series_id==series_id,Observation.day==data.day)):
        raise HTTPException(409,'该日期已有观测，请核对后重试')
    row=Observation(series_id=series_id,**data.model_dump())
    db.add(row)
    return row
