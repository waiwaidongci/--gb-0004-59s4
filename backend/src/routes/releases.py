from fastapi import APIRouter,Depends
from sqlalchemy import select
from src.config.database import session
from src.middlewares.auth import current_user,require
from src.models import Release
from src.schemas.release import ReleaseInput
from src.controllers.release_controller import create
from src.utils.serializers import serialize
router=APIRouter(prefix='/releases',tags=['releases'])
@router.get('')
def listing(db=Depends(session),user=Depends(current_user)): return [serialize(x) for x in db.scalars(select(Release).order_by(Release.id.desc()))]
@router.post('',status_code=201)
def creating(data:ReleaseInput,db=Depends(session),user=Depends(require('admin'))): return create(db,data,user)
