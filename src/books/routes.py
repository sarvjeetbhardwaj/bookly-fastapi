from fastapi import APIRouter, status
from typing import List
from fastapi import Header
from src.books.schemas import Book, BookUpdateModel
from src.books.book_data import book_list
from fastapi.exceptions import HTTPException


book_router = APIRouter()

@book_router.get('/books', response_model=List[Book], status_code=status.HTTP_200_OK)
def get_all_books():
    return book_list

@book_router.get('/books/{id}', response_model=BookUpdateModel, status_code=status.HTTP_200_OK)
def get_all_books(id:int):
    for book in book_list:
        if book['id'] == id:
            return book
        
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

@book_router.post('/create_book',response_model=BookUpdateModel, status_code=status.HTTP_201_CREATED)
def create_book(book:Book)->dict:
    new_book = book.model_dump()

    book_list.append(new_book)

    return new_book

@book_router.patch('/update_book/{id}',response_model=BookUpdateModel, status_code=status.HTTP_202_ACCEPTED)
def update_book(id:int ,book_update_data:BookUpdateModel):
    for book in book_list:
        if book['id'] == id:
            book['title'] = book_update_data.title
            book['author'] = book_update_data.author
            book['page_count'] = book_update_data.page_count
            book['publisher'] = book_update_data.publisher
            book['language'] = book_update_data.language

        
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')
        

@book_router.delete('/delete_book/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(id:int):
    for book in book_list:
        if book['id'] == id:
            book_list.remove(book)
            return status.HTTP_204_NO_CONTENT
        
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

    




