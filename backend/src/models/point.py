from datetime import date
from sqlalchemy import ForeignKey,Date,Float,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ForecastPoint(Base):
    __tablename__='forecast_points'
    __table_args__=(UniqueConstraint('run_id','day',name='uq_run_day'),)
    id:Mapped[int]=mapped_column(primary_key=True)
    run_id:Mapped[int]=mapped_column(ForeignKey('forecast_runs.id'))
    day:Mapped[date]=mapped_column(Date)
    predicted:Mapped[float]=mapped_column(Float)
    lower:Mapped[float]=mapped_column(Float)
    upper:Mapped[float]=mapped_column(Float)
