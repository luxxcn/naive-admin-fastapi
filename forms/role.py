from typing import Annotated
from fastapi import Query

from forms.base import PageForm


class RolePageForm(PageForm):
    """角色分页查询表单"""
    name: str | None = None


RolePageFormDep = Annotated[RolePageForm, Query()]
