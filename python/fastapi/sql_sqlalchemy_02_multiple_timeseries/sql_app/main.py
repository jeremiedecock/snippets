from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/values/", response_model=schemas.TimeSeries)
def create_ts_value(ts: schemas.TimeSeries, db: Session = Depends(get_db)):
    db_value = crud.get_ts_value_by_name_and_datetime(db, name=ts.name, datetime=ts.datetime)
    if db_value:
        raise HTTPException(status_code=400, detail="The (name, datetime) tuple is already registered")
    return crud.create_ts_value(db=db, ts=ts)


@app.get("/values/", response_model=list[schemas.TimeSeries])
def read_ts_value(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    values = crud.get_ts_value(db, skip=skip, limit=limit)
    return values
