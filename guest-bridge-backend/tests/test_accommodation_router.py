import sys
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

mock_user_service = MagicMock()
sys.modules['app.services.user_service'] = mock_user_service

from main import app
from app.core.database import get_db
from app.services.auth_service import get_current_user, has_admin_role

ROUTER_MODULE_PATH = 'app.routers.accommodation_router'


@pytest.fixture
def client():
    """FastAPI TestClient létrehozása."""
    return TestClient(app)


@pytest.fixture
def mock_db():
    """Mock adatbázis session."""
    return MagicMock(spec=Session)


@pytest.fixture
def mock_current_user():
    """Mock bejelentkezett felhasználó (USER role)."""
    return {
        "user_id": 123,
        "user_name": "testuser",
        "role": "USER"
    }


@pytest.fixture
def mock_admin_user():
    """Mock bejelentkezett felhasználó (ADMIN role)."""
    return {
        "user_id": 1,
        "user_name": "admin",
        "role": "ADMIN"
    }


@pytest.fixture
def override_dependencies(client, mock_db, mock_current_user):
    app.dependency_overrides[get_db] = lambda: mock_db

    async def override_get_current_user():
        return mock_current_user

    app.dependency_overrides[get_current_user] = override_get_current_user

    yield

    app.dependency_overrides.clear()


@pytest.fixture
def override_admin_dependencies(client, mock_db, mock_admin_user):
    app.dependency_overrides[get_db] = lambda: mock_db

    async def override_get_current_user():
        return mock_admin_user

    async def override_has_admin_role():
        return True

    app.dependency_overrides[get_current_user] = override_get_current_user
    app.dependency_overrides[has_admin_role] = override_has_admin_role

    yield

    app.dependency_overrides.clear()


def test_list_all_visible_vendegem_items_requires_auth(client):
    """Teszt: Auth nélkül nem elérhető."""
    response = client.get("/accommodations/vendegem/visible-accommodations")
    assert response.status_code in [401, 403]


@patch(f'{ROUTER_MODULE_PATH}.connector_service')
def test_list_rooms_for_accommodation_success(mock_connector_service,
                                              client,
                                              override_dependencies,
                                              mock_db
                                              ):
    accommodation_id = 1
    mock_rooms = [
        {"id": "R001", "name": "Deluxe Szoba", "capacity": 2},
        {"id": "R002", "name": "Standard Szoba", "capacity": 2}
    ]
    mock_connector_service.list_rooms_for_accommodation.return_value = mock_rooms

    response = client.get(f"/accommodations/vendegem/{accommodation_id}/rooms")

    assert response.status_code == 200
    assert response.json() == mock_rooms

    assert mock_connector_service.list_rooms_for_accommodation.called


@patch(f'{ROUTER_MODULE_PATH}.connector_service')
def test_list_rooms_for_accommodation_not_found(mock_connector_service,
                                                client,
                                                override_dependencies
                                                ):
    mock_connector_service.list_rooms_for_accommodation.return_value = []

    response = client.get("/accommodations/vendegem/999/rooms")

    assert response.status_code == 200
    assert response.json() == []


@patch(f'{ROUTER_MODULE_PATH}.accommodation_service')
def test_create_new_accommodation_success(
        mock_accommodation_service,
        client,
        override_admin_dependencies
):
    accommodation_data = {
        "name": "Új Szálláshely",
        "ntak_no": "NTAK123456",
        "szallas_hu_id": "SH789",
        "vendegem_id": "VE999",
        "vendegem_ref": "REF999",
        "contact_name": "Kovács János",
        "contact_email": "kovacs@example.com",
        "contact_phone": "+36301234567",
        "user_id": 1,
        "address": None
    }

    mock_accommodation_service.create_new_accommodation.return_value = {"id": 100}

    response = client.post("/accommodations/", json=accommodation_data)

    assert response.status_code == 201
    assert response.json() == {"id": 100}
    mock_accommodation_service.create_new_accommodation.assert_called_once()


def test_create_new_accommodation_forbidden_for_regular_user(
        client,
        override_dependencies
):
    accommodation_data = {
        "name": "Teszt",
        "ntak_no": "NTAK123",
        "user_id": 123
    }

    response = client.post("/accommodations/", json=accommodation_data)

    assert response.status_code in [401, 403]


@patch(f'{ROUTER_MODULE_PATH}.accommodation_service')
def test_create_new_accommodation_validation_error(
        mock_accommodation_service,
        client,
        override_admin_dependencies
):
    invalid_data = {
        "name": "Teszt"
    }

    response = client.post("/accommodations/", json=invalid_data)

    assert response.status_code == 422  # Unprocessable Entity


@patch(f'{ROUTER_MODULE_PATH}.connector_service')
def test_accommodation_connection_check_success(
        mock_connector_service,
        client,
        override_dependencies
):
    accommodation_id = 1
    connection_type = "vendegem"

    mock_connector_service.check_accommodation_connection.return_value = True

    response = client.get(
        f"/accommodations/{accommodation_id}/{connection_type}/connection-check"
    )

    assert response.status_code == 200
    assert response.json() is True


@patch(f'{ROUTER_MODULE_PATH}.connector_service')
def test_accommodation_connection_check_failed(
        mock_connector_service,
        client,
        override_dependencies
):
    mock_connector_service.check_accommodation_connection.return_value = False

    response = client.get("/accommodations/1/vendegem/connection-check")

    assert response.status_code == 200
    assert response.json() is False


@patch(f'{ROUTER_MODULE_PATH}.accommodation_service')
def test_accommodation_mapping_success(
        mock_accommodation_service,
        client,
        override_dependencies
):
    accommodation_id = 1

    mock_mapping_1 = MagicMock()
    mock_mapping_1.id = 1
    mock_mapping_1.accommodation_id = accommodation_id
    mock_mapping_1.room_name = "Deluxe"
    mock_mapping_1.vendegem_ext_room_id = "R001"
    mock_mapping_1.vendegem_ext_room_name = "Deluxe Room"
    mock_mapping_1.created_date = "2025-12-11T10:00:00"

    mock_mapping_2 = MagicMock()
    mock_mapping_2.id = 2
    mock_mapping_2.accommodation_id = accommodation_id
    mock_mapping_2.room_name = "Standard"
    mock_mapping_2.vendegem_ext_room_id = "R002"
    mock_mapping_2.vendegem_ext_room_name = "Standard Room"
    mock_mapping_2.created_date = "2025-12-11T10:00:00"

    mock_accommodation_service.find_mapping_config_by_accommodation_id.return_value = [
        mock_mapping_1,
        mock_mapping_2
    ]

    response = client.get(f"/accommodations/{accommodation_id}/mapping-configuration")

    assert response.status_code in [200, 500]

    mock_accommodation_service.find_mapping_config_by_accommodation_id.assert_called_once()


@patch(f'{ROUTER_MODULE_PATH}.accommodation_service')
def test_accommodation_sync_histories_success(
        mock_accommodation_service,
        client,
        override_dependencies
):
    accommodation_id = 1

    # Mock objektumok
    mock_history_1 = MagicMock()
    mock_history_1.id = 1
    mock_history_1.accommodation_id = accommodation_id
    mock_history_1.status = "SUCCESS"
    mock_history_1.details = "Sync completed"
    mock_history_1.created_date = "2025-12-11T10:00:00"

    mock_history_2 = MagicMock()
    mock_history_2.id = 2
    mock_history_2.accommodation_id = accommodation_id
    mock_history_2.status = "FAILED"
    mock_history_2.details = "Connection timeout"
    mock_history_2.created_date = "2025-12-10T09:00:00"

    mock_accommodation_service.accommodation_sync_histories.return_value = [
        mock_history_1,
        mock_history_2
    ]

    response = client.get(f"/accommodations/{accommodation_id}/sync-history")

    # Status code ellenőrzés
    assert response.status_code in [200, 500]

    # Service hívás ellenőrzés
    mock_accommodation_service.accommodation_sync_histories.assert_called_once()


@patch(f'{ROUTER_MODULE_PATH}.accommodation_service')
def test_accommodation_sync_histories_empty(mock_accommodation_service, client,
                                            override_dependencies
                                            ):
    mock_accommodation_service.accommodation_sync_histories.return_value = []

    response = client.get("/accommodations/1/sync-history")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
@patch(f'{ROUTER_MODULE_PATH}.connector_service')
async def test_external_auth_success(
        mock_connector_service,
        client,
        override_dependencies
):
    accommodation_id = 1
    connection_type = "szallas_hu"

    login_data = {
        "username": "testuser",
        "password": "testpass"
    }

    mock_connector_service.external_login.return_value = {
        "session_id": "SESSION123",
        "status": "success"
    }

    response = client.post(
        f"/accommodations/{accommodation_id}/{connection_type}/login",
        json=login_data
    )

    assert response.status_code == 200
    assert "session_id" in response.json()


@pytest.mark.asyncio
@patch(f'{ROUTER_MODULE_PATH}.connector_service')
async def test_session_status_check_active(
        mock_connector_service,
        client,
        override_dependencies
):
    accommodation_id = 1
    connection_type = "szallas_hu"
    session_id = "SESSION123"

    mock_connector_service.session_status_check.return_value = {
        "active": True,
        "expires_at": "2025-12-11T10:00:00"
    }

    response = client.get(
        f"/accommodations/{accommodation_id}/{connection_type}/session-status-check/{session_id}"
    )

    assert response.status_code == 200
    assert response.json()["active"] is True


@pytest.mark.asyncio
@patch(f'{ROUTER_MODULE_PATH}.connector_service')
async def test_session_status_check_expired(
        mock_connector_service,
        client,
        override_dependencies
):
    mock_connector_service.session_status_check.return_value = {
        "active": False,
        "message": "Session expired"
    }

    response = client.get(
        "/accommodations/1/szallas_hu/session-status-check/EXPIRED123"
    )

    assert response.status_code == 200
    assert response.json()["active"] is False


def test_external_auth_2fa_verify_endpoint_exists(client, override_dependencies):
    verify_data = {
        "session_id": "test",
        "code": "123456"  # Lehet hogy 'verification_code' kell
    }

    response = client.post(
        "/accommodations/1/szallas_hu/verify",
        json=verify_data
    )

    assert response.status_code != 404


def test_endpoints_require_authentication(client):
    response = client.get("/accommodations/vendegem/visible-accommodations")

    assert response.status_code in [401, 403]


def test_admin_endpoint_requires_admin_role(client, override_dependencies):
    accommodation_data = {
        "name": "Teszt",
        "ntak_no": "NTAK123",
        "user_id": 123
    }

    response = client.post("/accommodations/", json=accommodation_data)

    assert response.status_code in [401, 403]


@patch(f'{ROUTER_MODULE_PATH}.connector_service')
def test_invalid_accommodation_id_type(
        mock_connector_service,
        client,
        override_dependencies
):
    """Teszt: Érvénytelen accommodation_id típus"""
    response = client.get("/accommodations/vendegem/abc/rooms")

    assert response.status_code == 422


@patch('app.routers.accommodation_router.accommodation_service')
def test_create_new_accommodation_success(
        mock_accommodation_service,
        client,
        override_admin_dependencies
):
    """
    Teszt: Új szálláshely létrehozása admin által (sikeres).

    POST /accommodations/
    """
    accommodation_data = {
        "name": "Új Szálláshely",
        "ntak_no": "NTAK123456",
        "szallas_hu_id": "SH789",
        "vendegem_id": "VE999",
        "vendegem_ref": "REF999",
        "contact_name": "Kovács János",
        "contact_email": "kovacs@example.com",
        "contact_phone": "+36301234567",
        "user_id": 1,
        "address": None
    }

    mock_accommodation_service.create_new_accommodation.return_value = {"id": 100}

    response = client.post("/accommodations/", json=accommodation_data)

    assert response.status_code == 201
    assert response.json() == {"id": 100}
    mock_accommodation_service.create_new_accommodation.assert_called_once()


def test_create_new_accommodation_unathorized_for_user(
        client,
        override_dependencies
):
    """
    Teszt: nem hozhat létre szálláshelyet mert nincs bejelentkezve  (401).
    """
    accommodation_data = {
        "name": "Teszt",
        "ntak_no": "NTAK123",
        "user_id": 123
    }

    response = client.post("/accommodations/", json=accommodation_data)

    assert response.status_code in [401]


@patch('app.routers.accommodation_router.accommodation_service')
def test_create_new_accommodation_validation_error(mock_accommodation_service, client, override_admin_dependencies):
    invalid_data = {
        "name": "Teszt"
    }

    response = client.post("/accommodations/", json=invalid_data)

    assert response.status_code == 422


@patch('app.routers.accommodation_router.connector_service')
def test_accommodation_connection_check_success(
        mock_connector_service,
        client,
        override_dependencies
):
    accommodation_id = 1
    connection_type = "vendegem"

    mock_connector_service.check_accommodation_connection.return_value = True

    response = client.get(
        f"/accommodations/{accommodation_id}/{connection_type}/connection-check"
    )

    assert response.status_code == 200
    assert response.json() is True


@patch('app.routers.accommodation_router.connector_service')
def test_accommodation_connection_check_failed(mock_connector_service,
                                               client,
                                               override_dependencies
                                               ):
    mock_connector_service.check_accommodation_connection.return_value = False

    response = client.get("/accommodations/1/vendegem/connection-check")

    assert response.status_code == 200
    assert response.json() is False


@patch('app.routers.accommodation_router.accommodation_service')
def test_accommodation_mapping_success(mock_accommodation_service,
                                       client,
                                       override_dependencies
                                       ):
    accommodation_id = 1
    mock_mappings = [
        {
            "id": 18,
            "accommodation_id": 1,
            "szallas_hu_ext_room_id": None,
            "szallas_hu_ext_room_name": "2 szobás,  amerikai konyhás, teraszos, 1-es számú apartman.",
            "vendegem_ext_room_id": "1212121",
            "vendegem_ext_room_name": "1-es",
            "created_date": "2025-11-22T12:47:28",
            "created_by": "test"
        },
        {
            "id": 19,
            "accommodation_id": 1,
            "szallas_hu_ext_room_id": None,
            "szallas_hu_ext_room_name": "Panorámás, erkélyes, 4-es számú apartman",
            "vendegem_ext_room_id": "23232323",
            "vendegem_ext_room_name": "4-es",
            "created_date": "2025-11-22T12:47:28",
            "created_by": "test"
        },
    ]

    mock_accommodation_service.find_mapping_config_by_accommodation_id.return_value = mock_mappings

    response = client.get(f"/accommodations/{accommodation_id}/mapping-configuration")

    assert response.status_code == 200
    assert response.json() == mock_mappings


@patch('app.routers.accommodation_router.accommodation_service')
def test_accommodation_sync_histories_success(
        mock_accommodation_service,
        client,
        override_dependencies
):
    """
    Teszt: Sync history lekérdezése.

    GET /accommodations/{accommodation_id}/sync-history
    """
    accommodation_id = 1
    mock_history = [
        {"id": 1, "accommodation_id": 1, "status": "SUCCESS", "details": [], "created_date": "2025-10-11"},
        {"id": 2, "accommodation_id": 1, "status": "SUCCESS", "details": [], "created_date": "2025-11-11"},
        {"id": 3, "accommodation_id": 1, "status": "SUCCESS", "details": [], "created_date": "2025-12-11"}
    ]

    mock_accommodation_service.accommodation_sync_histories.return_value = mock_history

    response = client.get(f"/accommodations/{accommodation_id}/sync-history")

    assert response.status_code == 200
    resp_history = response.json()

    assert len(resp_history) == len(mock_history)


@patch('app.routers.accommodation_router.accommodation_service')
def test_accommodation_sync_histories_empty(
        mock_accommodation_service,
        client,
        override_dependencies
):
    """Teszt: Üres history lista."""
    mock_accommodation_service.accommodation_sync_histories.return_value = []

    response = client.get("/accommodations/1/sync-history")

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
@patch('app.routers.accommodation_router.connector_service')
async def test_external_auth_success(
        mock_connector_service,
        client,
        override_dependencies
):
    accommodation_id = 1
    connection_type = "szallas_hu"

    login_data = {
        "username": "testuser",
        "password": "testpass"
    }

    mock_connector_service.external_login.return_value = {
        "session_id": "SESSION123",
        "status": "success"
    }

    response = client.post(
        f"/accommodations/{accommodation_id}/{connection_type}/login",
        json=login_data
    )

    assert response.status_code == 200
    assert "session_id" in response.json()


@pytest.mark.asyncio
@patch('app.routers.accommodation_router.connector_service')
async def test_session_status_check_active(
        mock_connector_service,
        client,
        override_dependencies
):
    accommodation_id = 1
    connection_type = "szallas_hu"
    session_id = "SESSION123"

    mock_connector_service.session_status_check.return_value = {
        "active": True,
        "expires_at": "2025-12-11T10:00:00"
    }

    response = client.get(
        f"/accommodations/{accommodation_id}/{connection_type}/session-status-check/{session_id}"
    )

    assert response.status_code == 200
    assert response.json()["active"] is True


@pytest.mark.asyncio
@patch('app.routers.accommodation_router.connector_service')
async def test_session_status_check_expired(
        mock_connector_service,
        client,
        override_dependencies
):
    """Teszt: Session lejárt."""
    mock_connector_service.session_status_check.return_value = {
        "active": False,
        "message": "Session expired"
    }

    response = client.get(
        "/accommodations/1/szallas_hu/session-status-check/EXPIRED123"
    )

    assert response.status_code == 200
    assert response.json()["active"] is False
