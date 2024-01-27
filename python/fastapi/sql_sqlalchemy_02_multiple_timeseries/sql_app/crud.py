from sqlalchemy.orm import Session
from datetime import datetime

from . import models, schemas


def get_ts_value(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TimeSeries).offset(skip).limit(limit).all()


def get_ts_value_by_name_and_datetime(db: Session, name: str, datetime: datetime):
    return db.query(models.TimeSeries).filter(models.TimeSeries.datetime == datetime, models.TimeSeries.name == name).first()


def create_ts_value(db: Session, ts: schemas.TimeSeries):
    db_value = models.TimeSeries(name=ts.name, datetime=ts.datetime, value=ts.value)
    db.add(db_value)
    db.commit()
    db.refresh(db_value)
    return db_value
