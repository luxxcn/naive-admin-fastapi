import datetime
from typing import List, Optional
from sqlmodel import Field, select, Relationship, func

from models import SQLModel, DatabaseDep, PageResult, db_autocommit
from models.user.profile import Profile
from models.user.user_role import UserRole
from forms.user import UserPageFormDep
from libs.error import model_dump


class User(SQLModel, table=True):
    """用户"""

    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, max_length=50, unique=True)
    # password: str = Field(exclude=True)
    hashed_password: str = Field(default="", max_length=255, exclude=True)
    enable: bool = Field(default=True)
    create_time: int = Field(default=0, exclude=True)
    update_time: int = Field(default=0, exclude=True)
    profile: Profile = Relationship(back_populates="user")
    roles: List["Role"] = Relationship(back_populates="users",
                                       link_model=UserRole)
    current_role: Optional[int] = Field(default=None, exclude=True)

    def keys(self):
        return ["createTime", "updateTime", "profile", "roles", "currentRole"]

    @property
    def password(self):
        return ""

    @password.setter
    def password(self, val):
        from libs.auth import get_password_hash
        self.hashed_password = get_password_hash(val)

    @property
    def currentRole(self):
        from models.user.role import Role
        if self.current_role is None or len(self.roles) <= self.current_role:
            return Role(code="USER", name="用户")
        return self.roles[self.current_role]

    @currentRole.setter
    def currentRole(self, role_code: str):
        self.current_role = None
        for index, role in enumerate(self.roles):
            if role.code == role_code.upper():
                self.current_role = index
                break

    def switch_role(self, role_code: str):
        with db_autocommit():
            self.currentRole = role_code

    @property
    def createTime(self):
        return datetime.datetime.fromtimestamp(self.create_time).isoformat()

    @property
    def updateTime(self):
        return datetime.datetime.fromtimestamp(self.update_time).isoformat()

    @classmethod
    def get_user(cls, username: str, db: DatabaseDep):
        return db.exec(select(cls).filter_by(username=username)).first()

    @classmethod
    def get_users(cls, db: DatabaseDep):
        res = db.exec(select(cls)).all()
        res = model_dump(res)
        for user in res:
            for role in user["roles"]:
                role.pop("permissionIds")
        return res

    @classmethod
    def pagination_query(cls, form: UserPageFormDep, db: DatabaseDep):
        """分页查询"""
        offset = form.pageSize * (form.pageNo - 1)
        statement = select(cls)
        if form.username:
            statement = statement.where(cls.username == form.username)
        total = db.exec(
            select(func.count()).select_from(statement.subquery())).first()
        res = db.exec(statement.offset(offset).limit(form.pageSize)).all()
        res = [u.dumps() for u in res]
        for r in res:
            r.update(r["profile"])
            del r["profile"]
            del r["currentRole"]
        return PageResult(total=total, pageData=res)
