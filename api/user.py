from typing import Annotated
from fastapi import APIRouter, Depends

from libs.error_code import Success
from libs.auth import login_required, GetCurrentUserDep
from models.user.user import User

api = APIRouter(prefix="/user")


@api.get("")
async def get_users(data: Annotated[list, Depends(User.pagination_query)],
                    _: login_required):
    """获取用户列表"""
    return Success(data=data)


@api.post("")
async def create_user(_: login_required):
    """创建用户"""
    return Success(data={"id": 1})


@api.get("/detail")
async def detail(user: GetCurrentUserDep):
    """用户详情"""
    return Success(data=user)


@api.delete("/{id}")
async def delete_user(id: int, _: login_required):
    """删除用户"""
    return Success(data=id)


@api.patch("/{id}")
async def update_user(id: int, _: login_required):
    """修改用户"""
    return Success(data=id)


@api.patch("/password/reset/{id}")
async def reset_password(id: int, _: login_required):
    """重置密码"""
    return Success(data=id)
