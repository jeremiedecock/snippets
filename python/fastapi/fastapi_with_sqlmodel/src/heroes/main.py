#!/usr/bin/env python3

# Src: https://sqlmodel.tiangolo.com/tutorial/fastapi/simple-hero-api/

# To run this code, type: `uvicorn main:app`

from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
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
app = FastAPI(lifespan=lifespan, root_path="/api")


# Create a hero Path Operation
@app.post("/")
def create_hero(hero: Hero):
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
        return hero


# Read all heroes Path Operation
@app.get("/")
def read_heroes():
    with Session(engine) as session:
        heroes = session.exec(select(Hero)).all()
        return heroes


# Read a hero by ID Path Operation
@app.get("/{id}")
def read_hero(hero_id: int):
    """
    Get hero by ID.
    """
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        # heroes = session.exec(select(Hero).where(Hero.id == hero_id)).all()
        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        return hero
        #return heroes[0]


# Update a hero by ID Path Operation
@app.put("/{id}")
def update_hero(hero_id: int, hero: Hero):
    with Session(engine) as session:
        hero_db = session.get(Hero, hero_id)
        if hero_db is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_db.name = hero.name
        hero_db.secret_name = hero.secret_name
        hero_db.age = hero.age
        session.add(hero_db)
        session.commit()
        session.refresh(hero_db)
        return hero_db


# Delete a hero by ID Path Operation
@app.delete("/{id}")
def delete_hero(hero_id: int):
    with Session(engine) as session:
        hero = session.get(Hero, hero_id)
        if hero is None:
            raise HTTPException(status_code=404, detail="Hero not found")
        session.delete(hero)
        session.commit()
        return {"message": "Hero deleted successfully"}
