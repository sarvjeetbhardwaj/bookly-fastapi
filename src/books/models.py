from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime as dt, date
import uuid


class Book(SQLModel, table=True):
    __tablename__ = 'books'
    uid : uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    title : str
    author : str
    publisher : str
    published_date : date
    page_count : int
    language : str
    created_at : dt = Field(sa_column=Column(pg.TIMESTAMP, default = dt.now))
    updated_at : dt = Field(sa_column=Column(pg.TIMESTAMP, default = dt.now))

    def __repr__(self):
        return f'Book {self.title}'