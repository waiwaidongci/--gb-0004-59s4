from datetime import timedelta
from sqlalchemy import select,delete
from fastapi import HTTPException
from src.models import ForecastRun,ForecastPoint,Observation
from src.config.queue import queue,QUEUE_NAME
from src.utils.serializers import serialize
from .series_service import get_series
from .forecast_algorithm import forecast

def get_run(db,run_id):
    run=db.get(ForecastRun,run_id)
    if not run: raise HTTPException(404,'预测任务不存在')
    return run

def detail(db,run_id):
    run=get_run(db,run_id)
    data=serialize(run)
    data['points']=[serialize(x) for x in db.scalars(select(ForecastPoint).where(ForecastPoint.run_id==run_id).order_by(ForecastPoint.day))]
    data['series']=serialize(get_series(db,run.series_id))
    return data

def create_run(db,data,user):
    get_series(db,data.series_id)
    run=ForecastRun(**data.model_dump(),created_by=user.id)
    db.add(run); db.flush()
    return run

def enqueue(run_id): queue.rpush(QUEUE_NAME,str(run_id))

def compute(db,run_id):
    run=get_run(db,run_id)
    if run.status=='completed': return
    run.status='running'; db.commit()
    observations=list(db.scalars(select(Observation).where(Observation.series_id==run.series_id).order_by(Observation.day)))
    if any((b.day-a.day).days!=1 for a,b in zip(observations,observations[1:])):
        raise ValueError('序列日期不连续，请补齐缺失日再预测')
    result=forecast([x.value for x in observations],run.horizon,run.season)
    db.execute(delete(ForecastPoint).where(ForecastPoint.run_id==run_id))
    for i,point in enumerate(result.pop('points'),1):
        db.add(ForecastPoint(run_id=run_id,day=observations[-1].day+timedelta(days=i),**point))
    run.result=result; run.status='completed'; run.error=None
    db.commit()
