from typing import Optional
from sqlmodel import Field, Relationship

from models import SQLModel


class Profile(SQLModel, table=True):
    """用户资料"""

    id: int | None = Field(default=None, primary_key=True)
    userId: int = Field(foreign_key="user.id", exclude=True)
    user: "User" = Relationship(back_populates="profile")
    nickName: str = Field(index=True, max_length=50, unique=True)
    gender: Optional[int] = Field(default=None)
    avatar: str = Field(
        default=
        "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif?imageView2/1/w/80/h/80"
    )
    address: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
