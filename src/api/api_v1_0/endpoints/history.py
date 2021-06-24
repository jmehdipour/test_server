from fastapi import APIRouter

from data.connections.redis import get_redis_connection
from data.repositories.mongodb import get_sum_history

router = APIRouter()


@router.get("/history")
def get_history(offset: int = 0, limit: int = 10):
    history_items = get_sum_history(offset, limit)
    return history_items


@router.get("/total")
def get_total_sum():
    redis_conn = get_redis_connection()
    total_sum = redis_conn.get("total_sum")
    return {"total": total_sum}
