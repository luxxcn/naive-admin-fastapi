from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel as SQLModel_, Session, QueuePool, create_engine
from contextlib import contextmanager

from config.secure import DATABASE_URI

engine = create_engine(
    DATABASE_URI,
    poolclass=QueuePool,
    pool_size=10,
    pool_recycle=100,
    max_overflow=5,
    pool_timeout=30,
    pool_pre_ping=True,
)


@contextmanager
def db_autocommit():
    with Session(engine) as session:
        yield session
        session.commit()


def get_session():
    with Session(engine) as session:
        yield session
        session.commit()


DatabaseDep = Annotated[Session, Depends(get_session)]


class SQLModel(SQLModel_, table=False):
    """数据表模型"""

    def keys(self):
        return []

    def dumps(self):
        """让模型可以递归转dict"""
        res = self.model_dump()
        for k in self.keys():
            t = self.__getattribute__(k)
            if isinstance(t, SQLModel):
                t = t.dumps()
            if isinstance(t, list):
                t = [i.dumps() if isinstance(i, SQLModel) else i for i in t]
            res.update({k: t})
        return res


class PageResult(SQLModel, table=False):
    """分页查询结果"""
    total: int = 0
    pageData: list = []


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
