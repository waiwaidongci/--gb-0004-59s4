from datetime import date
from sqlalchemy import ForeignKey,UniqueConstraint,Date,Float
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class Observation(Base):
    __tablename__='observations'
    __table_args__=(UniqueConstraint('series_id','day',name='uq_series_day'),)
    id:Mapped[int]=mapped_column(primary_key=True)
    series_id:Mapped[int]=mapped_column(ForeignKey('series.id'))
    day:Mapped[date]=mapped_column(Date)
    value:Mapped[float]=mapped_column(Float)
