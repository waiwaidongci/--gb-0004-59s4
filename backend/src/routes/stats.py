from fastapi import APIRouter,Depends
from sqlalchemy import select,func
from src.config.database import session
from src.middlewares.auth import current_user
from src.models import Series,Observation,ForecastRun,Release
router=APIRouter()
@router.get('/stats')
def stats(db=Depends(session),user=Depends(current_user)):
    return {name:db.scalar(select(func.count()).select_from(model)) for name,model in [('series',Series),('observations',Observation),('runs',ForecastRun),('releases',Release)]}
