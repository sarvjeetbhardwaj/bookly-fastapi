from fastapi import FastAPI,status
from src.books.routes import book_router
from contextlib import asynccontextmanager
from src.db.create_engine import init_db
from src.config import config
from src.auth.routes import auth_router
from src.review.routes import review_router
from src.errors import UserAlreadyExists, create_exception_handler
from fastapi.responses import JSONResponse
from src.errors import register_all_errors
from src.middleware import register_middleware 

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

## Below needs to added for all the exception classes created in src.errors 
register_all_errors(app)

register_middleware(app)

@app.exception_handler(exc_class_or_status_code=500)
async def internal_server_error(request, exc):
    return JSONResponse(content={'message':'something went wrong', 'error_code': 'server_error'},
                            status_code=status)

app.include_router(book_router, tags=['books'])
app.include_router(auth_router, tags=['auth']) 
app.include_router(review_router, tags=['reviews']) 