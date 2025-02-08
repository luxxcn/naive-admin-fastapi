from typing import List
from sqlmodel import Field, Relationship, select, func

from models import DatabaseDep, SQLModel, PageResult
from models.user.user_role import UserRole
from models.permission.permission_role import PermissionRole
from forms.role import RolePageFormDep
from libs.auth import TokenDep


class Role(SQLModel, table=True):
    """角色"""
    id: int = Field(default=None, primary_key=True)
    code: str = Field(default="", max_length=50, unique=True)
    name: str = Field(default="", max_length=50, unique=True)
    enable: bool = Field(default=True)
    users: List["User"] = Relationship(back_populates="roles",
                                       link_model=UserRole)
    permissions: List["Permission"] = Relationship(back_populates="roles",
                                                   link_model=PermissionRole)

    def keys(self):
        return ["permissionIds"]

    @property
    def permissionIds(self):
        return [p.id for p in self.permissions]

    @classmethod
    def get_roles(cls, db: DatabaseDep):
        res = db.exec(select(cls)).all()
        return res

    @classmethod
    def get_permissions(cls, token: TokenDep, db: DatabaseDep):
        from models.permission.permission import Permission

        role = db.exec(select(cls).filter_by(code=token.role_code)).first()
        if not role:
            return None
        if not role.permissions and role.code == "SUPER_ADMIN":
            return Permission.get_permissions(db)

        # 构造权限树
        def filter_no_permission(p):
            p["children"] = [
                c for c in p["children"] if c["id"] in role.permissionIds
            ]
            for c in p["children"]:
                filter_no_permission(c)

        tree = [p.dumps() for p in role.permissions if p.parentId is None]
        for r in tree:
            filter_no_permission(r)
        return tree

    @classmethod
    def pagination_query(cls, form: RolePageFormDep, db: DatabaseDep):
        """分页查询"""
        offset = form.pageSize * (form.pageNo - 1)
        statement = select(cls)
        if form.name:
            statement = statement.where(cls.name == form.name)

        total = db.exec(
            select(func.count()).select_from(statement.subquery())).first()
        res = db.exec(statement.offset(offset).limit(form.pageSize)).all()
        res = [r.dumps() for r in res]

        return PageResult(total=total, pageData=res)
