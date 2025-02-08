from typing import Annotated
from fastapi import APIRouter, Depends

from libs.error_code import Success
from libs.auth import login_required
from models.user.role import Role

api = APIRouter(prefix="/role")


@api.get("/permissions/tree")
async def get_permissions(data: Annotated[list,
                                          Depends(Role.get_permissions)]):
    """角色权限树-by token"""
    return Success(data=data)


@api.get("")
async def get_roles(data: Annotated[list, Depends(Role.get_roles)],
                    _: login_required):
    """角色列表-all"""
    return Success(data=data)


@api.get("/page")
async def get_page(data: Annotated[list, Depends(Role.pagination_query)],
                   _: login_required):
    """角色列表-分页"""
    return Success(data=data)


@api.post("")
async def create_role(_: login_required):
    """新增角色"""
    return Success(data={"id": 1})


@api.delete("/{id}")
async def delete_role(id: int, _: login_required):
    """删除角色"""
    return Success(data=id)


@api.patch("/{id}")
async def update_role(id: int, _: login_required):
    """修改角色"""
    return Success(data=id)


@api.patch("/users/remove/{id}")
async def remove_user(id: int, _: login_required):
    """取消分配角色-批量"""
    return Success(data=id)


@api.patch("/users/add/{id}")
async def add_user(id: int, _: login_required):
    """分配角色-批量"""
    return Success(data=id)
