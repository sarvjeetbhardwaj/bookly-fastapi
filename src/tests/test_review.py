import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock

from fastapi import status
from src.main import app  # Adjust if your FastAPI app is in a different location

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.fixture
def mock_user():
    class UserObj:
        email = "test@example.com"
    return UserObj()

@pytest.mark.anyio
@patch("src.review.routes.ReviewService.add_review_to_book", new_callable=AsyncMock)
@patch("src.review.routes.get_current_user", new_callable=AsyncMock)
async def test_add_review_to_book(mock_get_current_user, mock_add_review_to_book, mock_user):
    mock_get_current_user.return_value = mock_user
    mock_add_review_to_book.return_value = {
        "review": "Great book!",
        "rating": 5,
        "user_email": "test@example.com",
        "book_uid": "book-uid-123"
    }
    payload = {
        "review": "Great book!",
        "rating": 5
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/review/book/book-uid-123", json=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["review"] == "Great book!"
    assert resp.json()["rating"] == 5
    assert resp.json()["user_email"] == "test@example.com"
    assert resp.json()["book_uid"] == "book-uid-123"