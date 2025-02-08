from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from contextlib import asynccontextmanager

from api import register_routers
from libs.error import APIException
from libs.error_code import ServerError, APIResponse
from models import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass


def create_app():
    app = FastAPI(title="g-spider", lifespan=lifespan)
    register_routers(app)
    return app


app = create_app()
web_path = Path("web")


@app.exception_handler(RequestValidationError)
async def pydantic_validation_exception_handler(request: Request,
                                                exc: RequestValidationError):
    resp = APIResponse(message=exc._errors,
                       code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return resp


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if not isinstance(exc, APIException):
        exc = APIException(exc.detail, exc.status_code)
    return exc.resp


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return ServerError(str(exc)).resp


@app.middleware("http")
async def api_and_static_middleware(request: Request, call_next):
    # 如果路径以 /api 开头，优先交给 FastAPI 的路由
    prefix = "/api"
    fastapi_files = ["/docs", "/openapi.json"]
    if request.url.path.startswith(
            prefix) or request.url.path in fastapi_files:
        return await call_next(request)

    # 静态文件处理
    file_path = web_path / request.url.path.lstrip("/")
    if file_path.exists() and file_path.is_file():
        return FileResponse(file_path)

    # 默认返回 index.html
    return FileResponse(web_path / "index.html")
