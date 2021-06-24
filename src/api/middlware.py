from fastapi import HTTPException

from config import get_settings


def is_admin(username: str, password: str):
    if not (username == get_settings().admin_username and password == get_settings().admin_password):
        raise HTTPException(status_code=403, detail="forbidden access")
