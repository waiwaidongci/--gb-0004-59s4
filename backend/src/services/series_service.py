from fastapi import HTTPException
from sqlalchemy import select,func
from src.models import Series,Observation
from src.utils.serializers import serialize

def list_series(db):
    rows=[]
    for item in db.scalars(select(Series).order_by(Series.id)):
        data=serialize(item)
        data['observation_count']=db.scalar(select(func.count()).select_from(Observation).where(Observation.series_id==item.id))
        data['total_demand']=round(db.scalar(select(func.sum(Observation.value)).where(Observation.series_id==item.id)) or 0,2)
        rows.append(data)
    return rows

def get_series(db,series_id):
    item=db.get(Series,series_id)
    if not item: raise HTTPException(404,'序列不存在')
    return item
