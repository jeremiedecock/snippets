from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

import hello
from hello import crud, models, schemas
from hello.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def check_api_token(req: Request):
    if "api-token" in req.headers:
        if req.headers["api-token"] != hello.cfg["api_token"]:
            raise HTTPException(status_code=401, detail="access denied")
    else:
        raise HTTPException(status_code=401, detail="missing Token")
    return True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/values/", response_model=schemas.TimeSeries)
def create_ts_value(ts: schemas.TimeSeries, db: Session = Depends(get_db), authorized: bool = Depends(check_api_token)):
    if authorized:
        db_value = crud.get_ts_value_by_name_and_datetime(db, name=ts.name, datetime=ts.datetime)
        if db_value:
            raise HTTPException(status_code=400, detail="The (name, datetime) tuple is already registered")
        return crud.create_ts_value(db=db, ts=ts)


@app.get("/values/", response_model=list[schemas.TimeSeries])
def read_ts_value(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), authorized: bool = Depends(check_api_token)):
    if authorized:
        values = crud.get_ts_value(db, skip=skip, limit=limit)
        return values
