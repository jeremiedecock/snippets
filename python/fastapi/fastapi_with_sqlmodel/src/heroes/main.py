#!/usr/bin/env python3

# Src: https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/

# To run this code, type: `uvicorn main:app`

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI
import functools
import logging
import os
from sqlmodel import Field, Session, SQLModel, create_engine, select


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',  # See https://docs.python.org/3/library/logging.html#logrecord-attributes
    datefmt=r'%Y-%m-%dT%H:%M:%S%z'
)


# Define the Hero model
class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    record_utc_datetime: datetime = Field(default_factory=functools.partial(datetime.now, timezone.utc), nullable=False)


SQLITE_DATABASE_URL = os.getenv("SQLITE_DATABASE_URL", "sqlite:////tmp/heroes.sqlite")
logging.info(f"Open {SQLITE_DATABASE_URL}")

# Create the database engine
engine = create_engine(
    url=SQLITE_DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False}
)


# Create Database and Tables on startup
# C.f. https://fastapi.tiangolo.com/advanced/events/#async-context-manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the database if it doesn't exist
    SQLModel.metadata.create_all(engine)
    yield


# Create the FastAPI app
app = FastAPI(lifespan=lifespan)


# Create Heroes Path Operation
@app.post("/heroes/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


# Read Heroes Path Operation
@app.get("/heroes/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes
