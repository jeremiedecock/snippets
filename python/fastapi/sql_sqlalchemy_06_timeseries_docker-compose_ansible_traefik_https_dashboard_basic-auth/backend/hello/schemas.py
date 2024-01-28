# The Pydantic models

from pydantic import BaseModel
from datetime import datetime


class TimeSeries(BaseModel):
    name: str
    datetime: datetime
    value: float

    class Config:
        from_attributes = True
        # orm_mode = True        # Replace "from_attributes = True" for older version of Pydantic