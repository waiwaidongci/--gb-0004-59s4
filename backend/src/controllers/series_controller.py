from sqlalchemy import select
from fastapi import HTTPException
from src.models import Series
from src.utils.serializers import serialize
from src.utils.audit import record

def create(db,data,user):
    if db.scalar(select(Series).where(Series.code==data.code)): raise HTTPException(409,'序列编码已存在')
    row=Series(**data.model_dump(),source_file='手工录入')
    db.add(row); db.flush(); record(db,user,'create_series',row.code); db.commit()
    return serialize(row)
