"""
初始化数据库(fake)
"""
import json
import time
from typing import List
from sqlmodel import select

from models import db_autocommit, create_db_and_tables
from models.user.user import User
from models.user.profile import Profile
from models.user.role import Role
from models.permission.permission import Permission


def _init_permissions():
    """权限表数据"""

    def to_permission(data: dict) -> List[Permission]:
        res = []
        for item in data:
            children = item.pop("children", None)
            if children:
                res.extend(to_permission(children))

            p = Permission(**item)
            # if p.parentId is None:
            #     p.parentId = 0
            res.append(p)
        return res

    with open("demo_data/permissions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        res = to_permission(data)
    first_menus = [p for p in res if p.parentId is None]
    other_menus = [p for p in res if p.parentId is not None]
    other_menus.sort(key=lambda x: x.id)
    with db_autocommit() as db:
        for p in first_menus:
            db.add(p)

    for p in other_menus:
        with db_autocommit() as db:
            db.add(p)


def _init_roles():
    """角色表数据"""
    data = [{
        "id": 1,
        "code": "SUPER_ADMIN",
        "name": "超级管理员",
        "enable": True
    }, {
        "id": 2,
        "code": "ROLE_QA",
        "name": "质检员",
        "enable": True
    }]
    with db_autocommit() as db:
        for item in data:
            db.add(Role(**item))
    with db_autocommit() as db:
        role = db.exec(select(Role).where(Role.id == 2)).first()
        permissions = db.exec(
            select(Permission).where(
                Permission.id.in_([1, 2, 3, 4, 5, 9, 10, 11, 12, 14,
                                   15]))).all()
        role.permissions.extend(permissions)


def _init_users():
    """用户表数据"""
    user_data = {
        "id": 1,
        "username": "admin",
        # "password": "123456",
        "enable": True,
        "create_time": int(time.time()),
        "update_time": int(time.time()),
    }

    with db_autocommit() as db:
        user = User(**user_data)
        user.password = "123456"
        db.add(user)
    profile_data = {
        "id": 1,
        "nickName": "Admin",
        "gender": None,
        "avatar":
        "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80",
        "address": None,
        "email": None,
        "userId": 1
    }
    with db_autocommit() as db:
        profile = Profile(**profile_data)
        db.add(profile)
    with db_autocommit() as db:
        user = db.exec(select(User).where(User.id == 1)).first()
        roles = db.exec(select(Role).where(Role.id.in_([1, 2]))).all()
        # 分配角色 超级管理员, 质检员
        user.roles.extend(roles)
        user.current_role = 0


def init_demo_data():
    # 创建表
    create_db_and_tables()
    # 示例数据
    # 权限
    _init_permissions()
    # 角色
    _init_roles()
    # 用户
    _init_users()
    print("done!")
