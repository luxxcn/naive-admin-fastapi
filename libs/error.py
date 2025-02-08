from pydantic import BaseModel
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from models import SQLModel


class APIException(HTTPException):
    """接口异常"""

    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "服务器错误，请稍后重试"
    error_code = 999
    data = None

    def __init__(self, message=None, code=None, error_code=None, data=None):
        if message:
            self.message = message
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if data:
            self.data = data
        super().__init__(self.code, self.message)
        self.resp = APIResponse(self.message, self.code, self.error_code,
                                self.data)


def model_dump(data):
    """模型转dict"""
    res = data
    if isinstance(data, list):
        res = [model_dump(r) for r in data]
    elif isinstance(data, SQLModel):
        res = data.dumps()
    elif isinstance(data, BaseModel):
        res = data.model_dump()

    return res


class APIResponse(JSONResponse):
    """接口返回内容封装"""

    code = status.HTTP_200_OK
    message = "OK"
    error_code = 0
    data = None

    def __init__(self, message=None, code=None, error_code=None, data=None):
        if message:
            self.message = message
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if data:
            self.data = model_dump(data)
        content = {"code": self.error_code, "message": self.message}
        if self.data:
            content.update({"data": self.data})
        super().__init__(content, self.code)
