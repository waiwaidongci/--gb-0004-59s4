from fastapi import HTTPException
from sqlalchemy import select
from src.models import Release
from .run_service import get_run

def publish(db,data,user):
    run=get_run(db,data.run_id)
    if run.status!='completed': raise HTTPException(409,'仅可发布已完成的预测')
    if db.scalar(select(Release).where(Release.run_id==run.id)): raise HTTPException(409,'此预测已发布')
    row=Release(**data.model_dump(),published_by=user.id)
    db.add(row); db.flush()
    return row
