from enum import Enum
from typing import Optional, List
from sqlmodel import Field, Relationship, select, and_
from sqlalchemy import Column, Boolean

from models import SQLModel, DatabaseDep
from models.permission.permission_role import PermissionRole


class PermissionType(str, Enum):
    MENU = "MENU"
    BUTTON = "BUTTON"
    API = "API"


class Permission(SQLModel, table=True):
    """权限"""
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default="", max_length=50)
    code: str = Field(default="", max_length=50, unique=True)
    type: PermissionType = Field(default=PermissionType.MENU)
    parentId: Optional[int] = Field(default=None, foreign_key="permission.id")
    parent: Optional["Permission"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={"remote_side": "Permission.id"})
    children: List["Permission"] = Relationship(back_populates="parent")
    path: str = Field(default="")
    redirect: str = Field(default="")
    icon: str = Field(default="")
    component: str = Field(default="")
    layout: str = Field(default="")
    keepAlive: bool = Field(default=False)
    method: str = Field(default="")
    description: str = Field(default="")
    show: bool = Field(default=True,
                       sa_column=Column(Boolean,
                                        default=True,
                                        comment="是否展示在页面菜单"))
    enable: bool = Field(default=True)
    order: int = Field(default=0)
    roles: List["Role"] = Relationship(back_populates="permissions",
                                       link_model=PermissionRole)

    def keys(self):
        return ["children"]

    @classmethod
    def get_permissions(cls, db: DatabaseDep):
        return db.exec(select(cls).where(cls.parentId == None)).all()

    @classmethod
    def get_button_permission_by_parent_id(cls, parentId: int,
                                           db: DatabaseDep):
        return db.exec(
            select(cls).where(
                and_(cls.parentId == parentId,
                     cls.type == PermissionType.BUTTON))).all()
