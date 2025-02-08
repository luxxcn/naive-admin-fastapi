from typing import Annotated
from fastapi import Query

from forms.base import PageForm


class UserPageForm(PageForm):
    """用户分页查询表单"""
    username: str | None = None


UserPageFormDep = Annotated[UserPageForm, Query()]
