from typing import Optional
from sqlmodel import SQLModel, Field


class PermissionRole(SQLModel, table=True):

    __tablename__ = "permission_role"
    permission_id: Optional[int] = Field(default=None,
                                         foreign_key="permission.id",
                                         primary_key=True)
    role_id: Optional[int] = Field(default=None,
                                   foreign_key="role.id",
                                   primary_key=True)
