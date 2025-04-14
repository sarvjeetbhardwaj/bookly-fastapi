from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.create_engine import init_db
from src.config import config
from src.auth.routes import auth_router

@asynccontextmanager
async def life_span(app:FastAPI): ## this defines which function/functions will run till what life span of the program
    #anything before yield will run at the start of the program
    #anything after yield will run at the end of the program
    print('server is starting')
    await init_db()
    yield
    print('server is stopped')

app = FastAPI(
    title = 'Bookly',
    description='A rest API for book review web service',
    version='v1',
    #lifespan=life_span
)

app.include_router(book_router, tags=['books'])
app.include_router(auth_router, tags=['auth']) 