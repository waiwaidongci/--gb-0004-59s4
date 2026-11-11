from fastapi import APIRouter,Depends
from fastapi.responses import Response
from sqlalchemy import select
from src.config.database import session
from src.middlewares.auth import current_user,require
from src.models import ForecastRun
from src.schemas.run import RunInput
from src.services.run_service import detail
from src.services.export_service import export_csv
from src.controllers.run_controller import create
from src.utils.serializers import serialize
router=APIRouter(prefix='/runs',tags=['forecasts'])
@router.get('')
def listing(db=Depends(session),user=Depends(current_user)):
    return [serialize(x) for x in db.scalars(select(ForecastRun).order_by(ForecastRun.id.desc()))]
@router.post('',status_code=201)
def creating(data:RunInput,db=Depends(session),user=Depends(require('admin','analyst'))): return create(db,data,user)
@router.get('/{run_id}')
def result(run_id:int,db=Depends(session),user=Depends(current_user)): return detail(db,run_id)
@router.get('/{run_id}/export')
def export(run_id:int,db=Depends(session),user=Depends(current_user)):
    return Response(export_csv(db,run_id),media_type='text/csv; charset=utf-8',headers={'Content-Disposition':f'attachment; filename="forecast-{run_id}.csv"'})
