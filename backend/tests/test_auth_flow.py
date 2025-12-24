from http import HTTPStatus
from uuid import uuid4

from sqlmodel import Session

from app.api.routes.user.schemas import UserCreate
from app.api.routes.user.service import create_user


def _create_test_user(*, session: Session, password: str) -> str:
    email = f"it-{uuid4().hex}@example.com"
    create_user(session=session, user_create=UserCreate(email=email, password=password))
    return email


async def test_login_success_and_read_me(client, db_session):  # noqa: ANN001
    password = "test-password-123"
    email = _create_test_user(session=db_session, password=password)

    resp = await client.post(
        "/api/v1/auth/access-token",
        data={"username": email, "password": password},
    )
    assert resp.status_code == HTTPStatus.OK
    assert resp.headers.get("X-Request-ID")

    payload = resp.json()
    assert "access_token" in payload
    assert payload.get("token_type") == "bearer"

    token = payload["access_token"]
    me = await client.get(
        "/api/v1/user/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me.status_code == HTTPStatus.OK
    assert me.headers.get("X-Request-ID")

    me_payload = me.json()
    assert me_payload["email"] == email
    assert "id" in me_payload


async def test_login_wrong_password_returns_standard_error(client, db_session):  # noqa: ANN001
    password = "test-password-123"
    email = _create_test_user(session=db_session, password=password)

    resp = await client.post(
        "/api/v1/auth/access-token",
        data={"username": email, "password": "wrong-password"},
    )
    assert resp.status_code == HTTPStatus.BAD_REQUEST
    assert resp.headers.get("X-Request-ID")

    payload = resp.json()
    assert payload["data"] is None
    assert payload["error"] == "HTTP_STATUS_ERROR"
    assert isinstance(payload["message"], str)


async def test_me_without_token_returns_standard_error(client):  # noqa: ANN001
    resp = await client.get("/api/v1/user/me")
    assert resp.status_code == HTTPStatus.UNAUTHORIZED
    assert resp.headers.get("X-Request-ID")

    payload = resp.json()
    assert payload["data"] is None
    assert payload["error"] == "HTTP_STATUS_ERROR"
    assert isinstance(payload["message"], str)
