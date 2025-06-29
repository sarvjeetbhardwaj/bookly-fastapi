import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi import status

from main import app  # Adjust if your FastAPI app is in a different location

@pytest.fixture
def anyio_backend():
    return "asyncio"

@pytest.mark.anyio
@patch("src.auth.routes.send_email.delay")
async def test_send_mail(mock_send_email):
    payload = {"email_addresses": ["test@example.com"]}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/send_mail", json=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] == "Email sent successfully"
    mock_send_email.assert_called_once()

@pytest.mark.anyio
@patch("src.auth.routes.UserService.user_exists", new_callable=AsyncMock)
@patch("src.auth.routes.UserService.create_user", new_callable=AsyncMock)
@patch("src.auth.routes.create_url_safe_token")
@patch("src.auth.routes.create_message")
@patch("src.auth.routes.mail.send_message")
async def test_create_user_account(
    mock_send_message, mock_create_message, mock_create_token, mock_create_user, mock_user_exists
):
    mock_user_exists.return_value = False
    mock_create_user.return_value = {"email": "test@example.com"}
    mock_create_token.return_value = "token"
    mock_create_message.return_value = MagicMock()
    payload = {
        "email": "test@example.com",
        "password": "password",
        "role": "user"
    }
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/signup", json=payload)
    assert resp.status_code == status.HTTP_201_CREATED
    assert "Account Created" in resp.json()["message"]

@pytest.mark.anyio
@patch("src.auth.routes.decode_url_safe_token")
@patch("src.auth.routes.UserService.get_user_by_email", new_callable=AsyncMock)
@patch("src.auth.routes.UserService.update_user", new_callable=AsyncMock)
async def test_verify_user_account_success(mock_update_user, mock_get_user_by_email, mock_decode_token):
    mock_decode_token.return_value = {"email": "test@example.com"}
    mock_get_user_by_email.return_value = {"email": "test@example.com"}
    mock_update_user.return_value = None
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/verify/token")
    assert resp.status_code == status.HTTP_200_OK
    assert "Account verified" in resp.json()["message"]

@pytest.mark.anyio
@patch("src.auth.routes.UserService.get_user_by_email", new_callable=AsyncMock)
@patch("src.auth.routes.verify_password")
@patch("src.auth.routes.create_access_token")
async def test_login_users_success(mock_create_access_token, mock_verify_password, mock_get_user_by_email):
    mock_get_user_by_email.return_value = MagicMock(email="test@example.com", password_hash="hash", uid="uid", role="user")
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "token"
    payload = {"email": "test@example.com", "password": "password"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/login", json=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["message"] == "Login_Successful"

@pytest.mark.anyio
@patch("src.auth.routes.RefreshTokenBearer.__call__", new_callable=AsyncMock)
@patch("src.auth.routes.create_access_token")
async def test_get_new_access_token(mock_create_access_token, mock_refresh_token_bearer):
    from datetime import datetime, timedelta
    now = datetime.now()
    mock_refresh_token_bearer.return_value = {
        "exp": (now + timedelta(hours=1)).timestamp(),
        "user": {"email": "test@example.com"}
    }
    mock_create_access_token.return_value = "new_token"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/refresh_token")
    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["access_token"] == "new_token"

@pytest.mark.anyio
@patch("src.auth.routes.create_url_safe_token")
@patch("src.auth.routes.create_message")
@patch("src.auth.routes.mail.send_message")
async def test_password_reset_request(mock_send_message, mock_create_message, mock_create_token):
    mock_create_token.return_value = "token"
    mock_create_message.return_value = MagicMock()
    payload = {"email": "test@example.com"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/password_reset_request", json=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert "Check your email" in resp.json()["message"]

@pytest.mark.anyio
@patch("src.auth.routes.decode_url_safe_token")
@patch("src.auth.routes.UserService.get_user_by_email", new_callable=AsyncMock)
@patch("src.auth.routes.UserService.update_user", new_callable=AsyncMock)
@patch("src.auth.routes.generate_password_hash")
async def test_reset_account_password_success(mock_generate_hash, mock_update_user, mock_get_user_by_email, mock_decode_token):
    mock_decode_token.return_value = {"email": "test@example.com"}
    mock_get_user_by_email.return_value = {"email": "test@example.com"}
    mock_generate_hash.return_value = "hashed"
    mock_update_user.return_value = None
    payload = {"new_password": "abc123", "confirm_new_password": "abc123"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.post("/password-verify/token", json=payload)
    assert resp.status_code == status.HTTP_200_OK
    assert "Password Reset Successfully" in resp.json()["message"]