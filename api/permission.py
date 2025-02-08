from typing import Annotated
from fastapi import APIRouter, Depends

from libs.error_code import Success
from libs.auth import login_required
from models.permission.permission import Permission

api = APIRouter(prefix="/permission")

GetPermissionDep = Annotated[list, Depends(Permission.get_permissions)]
GetButtonPermissionDep = Annotated[
    list, Depends(Permission.get_button_permission_by_parent_id)]


@api.get("/menu/tree")
async def get_menu_tree(data: GetPermissionDep, _: login_required):
    """权限树-菜单"""
    return Success(data=data)


@api.get("/tree")
async def get_tree(data: GetPermissionDep, _: login_required):
    """权限树-all"""
    return Success(data=data)


@api.post("")
async def create_permission(_: login_required):
    """新增权限"""
    return Success(data={"id": 1})


@api.delete("/{id}")
async def delete_role(id: int, _: login_required):
    """删除权限"""
    return Success(data=id)


@api.patch("/{id}")
async def update_permission(id: int, _: login_required):
    """修改权限"""
    return Success(data=id)


@api.get("/button/{parentId}")
async def get_button_permission(data: GetButtonPermissionDep,
                                _: login_required):
    """按钮权限-by parentId"""
    return Success(data=data)
