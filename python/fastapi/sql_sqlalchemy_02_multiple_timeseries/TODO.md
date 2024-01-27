# TODO

- [ ] Read and write the timezone in the datetime column
- [ ] Let the datetime be optional when writing a new record in the database
  - In the models.py module, use `default=func.now()` in datetime definition to tell SQLAlchemy to use the current datetime as the default value for the datetime column
  - e.g. `datetime = Column(DateTime(timezone=True), primary_key=True, default=func.now())`
- [ ] Let the datetime column be the index of the dataframe ?