from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime as dt
import uuid
from typing import Optional
from src.auth import models
from src.books import models


class Review(SQLModel, table=True):
    __tablename__ = 'reviews'
    uid : uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    rating : int = Field(lt=5)
    rating_text : str 
    user_uid : Optional[uuid.UUID] = Field(default=None, foreign_key='users.uid')
    book_uid : Optional[uuid.UUID] = Field(default=None, foreign_key='books.uid')
    created_at : dt = Field(sa_column=Column(pg.TIMESTAMP, default = dt.now))
    updated_at : dt = Field(sa_column=Column(pg.TIMESTAMP, default = dt.now))
    user: Optional["models.User"] = Relationship(back_populates='reviews')
    book: Optional["models.Book"] = Relationship(back_populates='reviews')

    def __repr__(self):
        return f'Review for {self.book_uid} by user {self.user_uid}'