"""
错误异常定义
"""

from fastapi import status
from libs.error import APIException, APIResponse


class Success(APIResponse):
    code = status.HTTP_200_OK
    error_code = 0


class CreateSuccess(Success):
    code = status.HTTP_201_CREATED
    error_code = 1


class DeleteSuccess(Success):
    code = status.HTTP_202_ACCEPTED
    error_code = 2


class ServerError(APIException):
    code = status.HTTP_500_INTERNAL_SERVER_ERROR
    message = "服务器内部错误，请稍后重试"
    error_code = 999


class ParameterException(APIException):
    code = status.HTTP_400_BAD_REQUEST
    message = "invalid parameter"
    error_code = 1000


class AuthFailed(APIException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = 1001
    message = "authorization failed"


class Forbidden(APIException):
    code = status.HTTP_403_FORBIDDEN
    error_code = 1003
    message = "forbidden, not in scope"


class NotFound(APIException):
    code = status.HTTP_404_NOT_FOUND
    message = "the resource are not found"
    error_code = 1004
