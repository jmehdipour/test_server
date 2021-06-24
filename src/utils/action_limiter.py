from enum import Enum

from fastapi.exceptions import HTTPException
from pydantic import conint
from starlette.requests import Request

from data.connections.redis import get_redis_connection


class ActivityType(str, Enum):
    sum = "sum"


class ActionLimiter:
    def __init__(
            self,
            activity_type: ActivityType,
            times: conint(ge=0) = 1,
            milliseconds: conint(ge=-1) = 0,
            seconds: conint(ge=-1) = 0,
            minutes: conint(ge=-1) = 0,
            hours: conint(ge=-1) = 0
    ):
        self.times = times
        self.milliseconds = milliseconds + 1000 * seconds + 60000 * minutes + 3600000 * hours
        self.activity_type = activity_type

    def __call__(self, request: Request):
        redis_conn = get_redis_connection()
        pipeline = redis_conn.pipeline()
        key = f"user:{request.client.host}:{self.activity_type.value}"
        pipeline.incrby(key, 1)
        pipeline.pttl(key)
        num, pexpire = pipeline.execute()
        if num == 1:
            redis_conn.pexpire(key, self.milliseconds)
        if num > self.times:
            raise HTTPException(429, "too many requests")

