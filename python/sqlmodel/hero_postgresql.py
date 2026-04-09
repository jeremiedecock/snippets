#!/usr/bin/env python3

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select

import secret

# This example is taken from https://sqlmodel.tiangolo.com/#example

# To connect to PostgreSQL: `podman exec -it postgres psql -h localhost -p 5432 -U user -d testdb`

# Create a SQLModel Model

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


# Create Rows

hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


# Write to the Database

DATABASE_URL = f"postgresql+psycopg2://{secret.DBUSER}:{secret.DBPASSWORD}@{secret.DBHOST}/{secret.DBNAME}"

engine = create_engine(DATABASE_URL)

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()


# Read all rows

with Session(engine) as session:
    statement = select(Hero)
    results = session.exec(statement)
    for hero in results:
        print(hero)


# Select from the Database

with Session(engine) as session:
    statement = select(Hero).where(Hero.name == "Rusty-Man").where(Hero.age == 48)
    hero = session.exec(statement).first()
    print("SELECT ... WHERE ...:", hero)
