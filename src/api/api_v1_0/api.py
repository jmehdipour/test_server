from fastapi import Depends, APIRouter

from api.api_v1_0.endpoints.math import router as math_router
from api.api_v1_0.endpoints.history import router as history_router
from api.middlware import is_admin

router = APIRouter()

router.include_router(math_router)
router.include_router(history_router, dependencies=[Depends(is_admin)])
