import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import status

from main import app  # Adjust if your FastAPI app is in a different location

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def mock_token():
    return {"user": {"user_uid": "test-user-uid"}}

@pytest.mark.anyio
@patch("src.books.routes.BookService.get_all_books", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_get_all_books(mock_token_bearer, mock_get_all_books, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_get_all_books.return_value = []
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/books")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

@pytest.mark.anyio
@patch("src.books.routes.BookService.get_user_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_get_user_book_submissions(mock_token_bearer, mock_get_user_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_get_user_book.return_value = []
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/user/test-user-uid")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == []

@pytest.mark.anyio
@patch("src.books.routes.BookService.create_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_create_book(mock_token_bearer, mock_create_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_create_book.return_value = {"title": "Test Book", "author": "Author", "user_uid": "test-user-uid"}
    payload = {"title": "Test Book", "author": "Author"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/create_book", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json()["title"] == "Test Book"

@pytest.mark.anyio
@patch("src.books.routes.BookService.get_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_get_book_found(mock_token_bearer, mock_get_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_get_book.return_value = {"title": "Test Book", "author": "Author", "user_uid": "test-user-uid"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/books/test-book-uid")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["title"] == "Test Book"

@pytest.mark.anyio
@patch("src.books.routes.BookService.get_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_get_book_not_found(mock_token_bearer, mock_get_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_get_book.return_value = None
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/books/unknown-uid")
    assert resp.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
@patch("src.books.routes.BookService.update_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_update_book_found(mock_token_bearer, mock_update_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_update_book.return_value = {"title": "Updated Book", "author": "Author", "user_uid": "test-user-uid"}
    payload = {"title": "Updated Book"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.patch("/update_book/test-book-uid", json=payload)
    assert resp.status_code == status.HTTP_202_ACCEPTED
    assert resp.json()["title"] == "Updated Book"

@pytest.mark.anyio
@patch("src.books.routes.BookService.update_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_update_book_not_found(mock_token_bearer, mock_update_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_update_book.return_value = None
    payload = {"title": "Updated Book"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.patch("/update_book/unknown-uid", json=payload)
    assert resp.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
@patch("src.books.routes.BookService.delete_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_delete_book_found(mock_token_bearer, mock_delete_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_delete_book.return_value = True
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.delete("/delete_book/test-book-uid")
    assert resp.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.anyio
@patch("src.books.routes.BookService.delete_book", new_callable=AsyncMock)
@patch("src.books.routes.TokenBearer.__call__", new_callable=AsyncMock)
async def test_delete_book_not_found(mock_token_bearer, mock_delete_book, mock_token):
    mock_token_bearer.return_value = mock_token
    mock_delete_book.return_value = None
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.delete("/delete_book/unknown-uid")
    assert resp.status_code == status.HTTP_404_NOT_FOUND