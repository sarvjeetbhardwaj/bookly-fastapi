from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import config
from src.books.models import Book
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker


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


async def get_session() ->AsyncSession:
    Session = sessionmaker(
        bind=engine, 
        class_ = AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session:
        yield session