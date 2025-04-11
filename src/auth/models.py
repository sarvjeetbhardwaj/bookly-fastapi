from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime as dt

class User(SQLModel, table=True):
    __tablename__ = 'users'
    uid : uuid.UUID = Field(sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4))
    username: str
    email : str
    first_name : str
    last_name : str
    is_verified: bool=Field(default=False)
    password_hash : str = Field(exclude=True)
    created_at : dt = Field(sa_column=Column(pg.TIMESTAMP, default = dt.now))
    updated_at : dt = Field(sa_column=Column(pg.TIMESTAMP, default = dt.now))

    def __repr__(self):
        return f'User {self.username}'