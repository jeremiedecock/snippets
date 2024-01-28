# The Pydantic models

from pydantic import BaseModel
from datetime import datetime


class TimeSeries(BaseModel):
    datetime: datetime
    value: float

    class Config:
        from_attributes = True