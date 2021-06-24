from starlette.requests import Request

from data.connections.redis import get_redis_connection


def get_user_error_count(request: Request):
    key = f"user:{request.client.host}:error"
    redis_conn = get_redis_connection()
    error_count = int(redis_conn.get(key)) or 0
    return error_count


def update_total_sum(new_value):
    redis_conn = get_redis_connection()
    redis_conn.incrby("total_sum", new_value)
    return True


def update_user_error_counter(request):
    milliseconds = 3600000 * 1  # 1 hour
    redis_conn = get_redis_connection()
    pipeline = redis_conn.pipeline()
    key = f"user:{request.client.host}:error"
    pipeline.incrby(key, 1)
    pipeline.pttl(key)
    num, pexpire = pipeline.execute()
    if num == 1:
        redis_conn.pexpire(key, milliseconds)