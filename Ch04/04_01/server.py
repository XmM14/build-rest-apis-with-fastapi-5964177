from datetime import datetime, timedelta

from fastapi import FastAPI
from pydantic import BaseModel, field_serializer

app = FastAPI()


class TimeResponse(BaseModel):
    delta: timedelta

    @field_serializer('delta')
    def serialize_timedelta(self, value: timedelta) -> float:
        return value.total_seconds()


@app.get('/time_delta')
def time_diff(start: datetime, end: datetime) -> TimeResponse:
    delta = end - start
    return TimeResponse(delta=delta)
