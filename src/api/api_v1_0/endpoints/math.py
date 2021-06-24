from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from data.repositories.mongodb import save_sum_in_db
from data.repositories.redis import update_total_sum
from config import get_settings
from utils.action_limiter import ActionLimiter, ActivityType

router = APIRouter()


@router.get(
    "/sum",
    dependencies=[
        Depends(ActionLimiter(ActivityType.sum, times=get_settings().request_limit_per_hour, hours=1))
    ]
)
def get_sum(a: int, b: int):
    try:
        sum_value = a + b
        save_sum_in_db(a, b, sum_value)
        update_total_sum(sum_value)
    except Exception as ex:
        raise HTTPException(status_code=500, detail="server internal error")
    return {"result": sum_value}
