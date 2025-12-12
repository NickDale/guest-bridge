from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.orm import Session


@pytest.fixture
def mock_db():
    """Mock adatbázis session."""
    return MagicMock(spec=Session)


@pytest.fixture
def valid_token_payload():
    """Érvényes token payload."""
    return {
        "id": 123,
        "sub": "balogh.norbert",
        "r": "USER"
    }


@pytest.fixture
def admin_token_payload():
    """Admin token payload."""
    return {
        "id": 1,
        "sub": "admin",
        "r": "ADMIN"
    }


@pytest.fixture
def mock_user():
    """Mock felhasználó objektum."""
    user = MagicMock()
    user.id = 123
    user.username = "testuser"
    user.full_name = "Test User"
    user.email = "test@example.com"
    user.blocked_date = None

    user_type = MagicMock()
    user_type.name = "user"
    user.user_type = user_type

    return user


@pytest.fixture
def blocked_user():
    user = MagicMock()
    user.id = 999
    user.username = "blockeduser"
    user.blocked_date = datetime(2025, 1, 1)

    user_type = MagicMock()
    user_type.name = "user"
    user.user_type = user_type

    return user


def test_create_access_token_with_default_expiration(valid_token_payload):
    """
    Teszt: Token létrehozása alapértelmezett lejárati idővel.
    """
    from app.services.auth_service import create_access_token, SECRET_KEY, ALGORITHM

    token = create_access_token(data=valid_token_payload)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded["id"] == 123
    assert decoded["sub"] == "balogh.norbert"
    assert decoded["r"] == "USER"
    assert "exp" in decoded


def test_create_access_token_with_custom_expiration(valid_token_payload):
    from app.services.auth_service import create_access_token, SECRET_KEY, ALGORITHM

    custom_expiration = timedelta(minutes=30)
    token = create_access_token(data=valid_token_payload, expires_delta=custom_expiration)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded is not None
    assert "exp" in decoded


def test_create_access_token_contains_all_required_fields(valid_token_payload):
    from app.services.auth_service import create_access_token, SECRET_KEY, ALGORITHM

    token = create_access_token(data=valid_token_payload)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert "id" in decoded
    assert "sub" in decoded
    assert "r" in decoded
    assert "exp" in decoded


def test_create_access_token_does_not_modify_original_data(valid_token_payload):
    """
    Teszt: A token létrehozása nem módosítja az eredeti adatokat.
    """
    from app.services.auth_service import create_access_token

    original_data = valid_token_payload.copy()
    create_access_token(data=valid_token_payload)

    # Az eredeti adat nem változott
    assert valid_token_payload == original_data
    assert "exp" not in valid_token_payload


def test_decode_access_token_with_expired_token(valid_token_payload):
    from app.services.auth_service import create_access_token, decode_access_token

    expired_token = create_access_token(
        data=valid_token_payload,
        expires_delta=timedelta(seconds=-10)
    )

    result = decode_access_token(expired_token)
    assert result is None


def test_decode_access_token_with_wrong_secret():
    from app.services.auth_service import decode_access_token, ALGORITHM

    wrong_secret = "wrong_secret_key"
    payload = {"id": 123, "sub": "test"}

    malicious_token = jwt.encode(payload, wrong_secret, algorithm=ALGORITHM)
    result = decode_access_token(malicious_token)

    assert result is None


@pytest.mark.asyncio
async def test_get_current_user_with_valid_token(valid_token_payload):
    """
    Teszt: Érvényes tokenből a felhasználó adatainak kinyerése.
    """
    from app.services.auth_service import create_access_token, get_current_user

    token = create_access_token(data=valid_token_payload)
    result = await get_current_user(token=token)

    assert result["user_id"] == 123
    assert result["user_name"] == "balogh.norbert"
    assert result["role"] == "USER"


@pytest.mark.asyncio
async def test_get_current_user_with_invalid_token():
    """
    Teszt: Érvénytelen token esetén 401 hibát dob.
    """
    from app.services.auth_service import get_current_user

    invalid_token = "invalid.token.here"

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=invalid_token)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_with_expired_token(valid_token_payload):
    """
    Teszt: Lejárt token esetén 401 hibát dob.
    """
    from app.services.auth_service import create_access_token, get_current_user

    expired_token = create_access_token(
        data=valid_token_payload,
        expires_delta=timedelta(seconds=-10)
    )

    with pytest.raises(HTTPException) as exc_info:
        await get_current_user(token=expired_token)

    assert exc_info.value.status_code == 401


@pytest.mark.asyncio
async def test_has_admin_role_with_admin_user(admin_token_payload):
    """
    Teszt: Admin felhasználó esetén True-t ad vissza.
    """
    from app.services.auth_service import create_access_token, has_admin_role

    token = create_access_token(data=admin_token_payload)
    result = await has_admin_role(token=token)

    assert result is True


@pytest.mark.asyncio
async def test_has_admin_role_with_regular_user(valid_token_payload):
    """
    Teszt: Nem admin felhasználó esetén 403 hibát dob.
    """
    from app.services.auth_service import create_access_token, has_admin_role

    token = create_access_token(data=valid_token_payload)

    with pytest.raises(HTTPException) as exc_info:
        await has_admin_role(token=token)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_has_admin_role_case_insensitive():
    """
    Teszt: Szerepkör ellenőrzés kis/nagybetű érzéketlen.
    """
    from app.services.auth_service import create_access_token, has_admin_role

    payload = {
        "id": 1,
        "sub": "admin",
        "r": "admin"  # kisbetűs
    }

    token = create_access_token(data=payload)
    result = await has_admin_role(token=token)

    assert result is True


def test_verify_user_access_admin_can_access_any_user():
    """
    Teszt: Admin bármely felhasználó adatához hozzáférhet.
    """
    from app.services.auth_service import verify_user_access

    admin_current_user = {
        "user_id": 1,
        "user_name": "admin",
        "role": "ADMIN"
    }

    result = verify_user_access(user_id=999, current_user=admin_current_user)

    assert result == admin_current_user


def test_verify_user_access_user_can_access_own_data():
    """
    Teszt: Felhasználó hozzáférhet a saját adataihoz.
    """
    from app.services.auth_service import verify_user_access

    current_user = {
        "user_id": 123,
        "user_name": "testuser",
        "role": "USER"
    }

    result = verify_user_access(user_id=123, current_user=current_user)

    assert result == current_user


def test_verify_user_access_user_cannot_access_others_data():
    """
    Teszt: Felhasználó NEM férhet hozzá más adataihoz.
    """
    from app.services.auth_service import verify_user_access

    current_user = {
        "user_id": 123,
        "user_name": "testuser",
        "role": "USER"
    }

    with pytest.raises(HTTPException) as exc_info:
        verify_user_access(user_id=999, current_user=current_user)

    assert exc_info.value.status_code == 403


@patch('app.services.auth_service.user_service')
def test_login_success(mock_user_service, mock_db, mock_user):
    """
    Teszt: Sikeres bejelentkezés.
    """
    from app.services.auth_service import login

    mock_user_service.login.return_value = mock_user

    result = login(username="testuser", password="password123", db=mock_db)

    assert "access_token" in result
    assert "token_type" in result
    assert result["token_type"] == "bearer"
    assert "user" in result
    assert result["user"]["id"] == 123


@patch('app.services.auth_service.user_service')
def test_login_invalid_credentials(mock_user_service, mock_db):
    """
    Teszt: Hibás credentials esetén 401 hibát dob.
    """
    from app.services.auth_service import login

    mock_user_service.login.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        login(username="wronguser", password="wrongpass", db=mock_db)

    assert exc_info.value.status_code == 401


@patch('app.services.auth_service.user_service')
def test_login_blocked_user(mock_user_service, mock_db, blocked_user):
    """
    Teszt: Blokkolt felhasználó nem tud bejelentkezni.
    """
    from app.services.auth_service import login

    mock_user_service.login.return_value = blocked_user

    with pytest.raises(HTTPException) as exc_info:
        login(username="blockeduser", password="password123", db=mock_db)

    assert exc_info.value.status_code == 403


@patch('app.services.auth_service.user_service')
def test_login_token_contains_correct_data(mock_user_service, mock_db, mock_user):
    """
    Teszt: A token tartalmazza a helyes adatokat.
    """
    from app.services.auth_service import login, SECRET_KEY, ALGORITHM

    mock_user_service.login.return_value = mock_user

    result = login(username="testuser", password="password123", db=mock_db)

    token = result["access_token"]
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded["id"] == 123
    assert decoded["sub"] == "testuser"
    assert decoded["r"] == "USER"


# ============================================================================
# 7. BIZTONSÁGI TESZTEK
# ============================================================================

def test_token_cannot_be_forged():
    """
    Teszt: Token nem hamisítható más SECRET_KEY-jel.
    """
    from app.services.auth_service import decode_access_token, ALGORITHM

    fake_secret = "hacker_secret"
    payload = {"id": 999, "sub": "hacker", "r": "ADMIN"}

    forged_token = jwt.encode(payload, fake_secret, algorithm=ALGORITHM)
    result = decode_access_token(forged_token)

    assert result is None


def test_create_access_token_with_empty_data():
    """
    Teszt: Üres adatokkal is működik.
    """
    from app.services.auth_service import create_access_token, SECRET_KEY, ALGORITHM

    empty_data = {}
    token = create_access_token(data=empty_data)

    assert token is not None
    assert isinstance(token, str)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert "exp" in decoded
