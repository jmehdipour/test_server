from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from api.api_v1_0.api import router as api_router_v1_0
from config import get_settings
from data.repositories.redis import get_user_error_count, update_user_error_counter

app = FastAPI(title=get_settings().app_name)

app.include_router(api_router_v1_0, prefix='/api_v1.0')


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    if exc.status_code in [405]:  # method not allowed, and bad data
        update_user_error_counter(request)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail)}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    update_user_error_counter(request)
    messages = []
    for e in exc.errors():
        loc = '>'.join([str(item) for item in e['loc']])
        messages.append(f"loc:'{loc}', type:'{e['type']}', msg:'{e['msg']}'")
    return JSONResponse(
        status_code=422,
        content={"detail": messages}
    )


@app.middleware("http")
async def http_middleware(request: Request, call_next):
    if get_user_error_count(request) > get_settings().error_limit_per_hour:
        return JSONResponse(
            status_code=403,
            content={"detail": "You are not allowed Because of make many errors"}
        )
    else:
        response = await call_next(request)
        return response


if get_settings().debug:
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host="127.0.0.1", port=8000, debug=True)
