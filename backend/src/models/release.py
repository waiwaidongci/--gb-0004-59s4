from datetime import datetime
from sqlalchemy import ForeignKey,String,DateTime
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class Release(Base):
    __tablename__='releases'
    id:Mapped[int]=mapped_column(primary_key=True)
    run_id:Mapped[int]=mapped_column(ForeignKey('forecast_runs.id'),unique=True)
    note:Mapped[str]=mapped_column(String(500))
    published_by:Mapped[int]=mapped_column(ForeignKey('users.id'))
    published_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
