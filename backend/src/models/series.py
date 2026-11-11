from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class Series(Base):
    __tablename__='series'
    id:Mapped[int]=mapped_column(primary_key=True)
    code:Mapped[str]=mapped_column(String(60),unique=True)
    name:Mapped[str]=mapped_column(String(100))
    city:Mapped[str]=mapped_column(String(40))
    product:Mapped[str]=mapped_column(String(60))
    unit:Mapped[str]=mapped_column(String(20),default='束')
    source_file:Mapped[str]=mapped_column(String(120))
