from datetime import datetime
from sqlalchemy import ForeignKey,String,JSON,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ForecastRun(Base):
    __tablename__='forecast_runs'
    id:Mapped[int]=mapped_column(primary_key=True)
    name:Mapped[str]=mapped_column(String(100))
    series_id:Mapped[int]=mapped_column(ForeignKey('series.id'))
    horizon:Mapped[int]=mapped_column(default=14)
    season:Mapped[int]=mapped_column(default=7)
    status:Mapped[str]=mapped_column(String(20),default='queued')
    result:Mapped[dict]=mapped_column(JSON,default=dict)
    error:Mapped[str|None]=mapped_column(String(500),nullable=True)
    created_by:Mapped[int]=mapped_column(ForeignKey('users.id'))
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
