# The SQLAlchemy models

from sqlalchemy import Column, DateTime, Float #, Integer

from .database import Base

class TimeSeries(Base):
    __tablename__ = "timeseries"

    datetime = Column(DateTime, primary_key=True)
    value = Column(Float)
