# The SQLAlchemy models

from sqlalchemy import Column, PrimaryKeyConstraint, DateTime, String, Float #, Integer

from hello.database import Base

class TimeSeries(Base):
    __tablename__ = "timeseries"

    name = Column(String)
    datetime = Column(DateTime)
    value = Column(Float)

    __table_args__ = (
        PrimaryKeyConstraint('name', 'datetime'),
    )
