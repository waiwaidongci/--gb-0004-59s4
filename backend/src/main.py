import os,logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import text
from src.config.database import Base,engine
from src.config.queue import queue
from src import models
from src.routes import auth,series,runs,releases,audits,stats
from src.middlewares.request_guard import RequestGuard
from src.middlewares.error_handler import ErrorHandler
@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    if os.getenv('SEED_DEMO','true').lower()=='true':
        try:
            from scripts.seed_demo import seed
            seed()
        except Exception: logging.exception('demo seed failed; service remains available')
    yield
app=FastAPI(title='潮汐需求预测席',lifespan=lifespan)
app.add_middleware(RequestGuard)
app.add_middleware(ErrorHandler)
for module in [auth,series,runs,releases,audits,stats]: app.include_router(module.router)
@app.get('/health')
def health():
    with engine.connect() as c: c.execute(text('SELECT 1'))
    queue.ping()
    return {'status':'healthy'}
