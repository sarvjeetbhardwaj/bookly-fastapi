from fastapi import APIRouter, status, Depends
from typing import List
from fastapi import Header
from src.books.schemas import Book, BookUpdateModel, BookCreateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from src.books.book_data import book_list
from fastapi.exceptions import HTTPException
from src.db.create_engine import get_session
from src.books.service import BookService

book_router = APIRouter()
book_service = BookService()

@book_router.get('/books', response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_all_books(session: AsyncSession = Depends(get_session)):
    books = await book_service.get_all_books(session=session)
    return books

@book_router.post('/create_book', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data:BookCreateModel, session: AsyncSession = Depends(get_session))->dict:
    new_book =  await book_service.create_book(book_data=book_data, session=session)
    return new_book

@book_router.get('/books/{book_uid}', status_code=status.HTTP_200_OK)
async def get_all_books(book_uid:str, session: AsyncSession = Depends(get_session)):
    book = await book_service.get_book(book_uid=book_uid, session=session)

    if book:
        return book
    else:    
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

@book_router.patch('/update_book/{book_uid}', status_code=status.HTTP_202_ACCEPTED)
async def update_book(book_uid:str ,book_update_data:BookUpdateModel,
                 session: AsyncSession = Depends(get_session)):
    
    updated_book = await book_service.update_book(book_uid=book_uid, update_book_data=book_update_data,
                                            session=session)
    if updated_book:
        return updated_book
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        

@book_router.delete('/delete_book/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:str,session: AsyncSession = Depends(get_session)):
    book_to_delete = await book_service.delete_book(book_uid=book_uid, session=session)

    if book_to_delete is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
    else:        
        return {}

    




