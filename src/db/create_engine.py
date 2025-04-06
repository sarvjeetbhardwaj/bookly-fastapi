from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config
from dotenv import load_dotenv
from src.books.models import Book


## thhis function creates a database engine
engine = AsyncEngine(
    create_engine(
        url = config.DATABASE_URL,
        echo=True,
    )
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
       