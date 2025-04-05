from fastapi import FastAPI
from src.books.routes import book_router

app = FastAPI(
    title = 'Bookly',
    description='A rest API for book review web service',
    version='v1'
)

app.include_router(book_router, tags=['books'])