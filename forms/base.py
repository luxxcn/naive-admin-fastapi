from pydantic import BaseModel


class PageForm(BaseModel):
    """分页查询表单"""

    pageNo: int = 1
    pageSize: int = 10
