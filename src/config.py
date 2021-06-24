from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    # app
    app_name: str = "Awesome API"
    debug: bool = True

    # mongodb
    mongo_url: str = "mongodb://localhost:27017/"
    mongo_db_name: str = "bomino"

    # redis
    redis_url: str = "redis://localhost/0"

    # admin credentials
    admin_username = "admin"
    admin_password = "admin"

    # rate limit
    error_limit_per_hour = 15
    request_limit_per_hour = 100


@lru_cache()
def get_settings():
    return Settings()
