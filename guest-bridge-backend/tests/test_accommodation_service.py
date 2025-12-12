from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException


@pytest.fixture
def mock_db():
    """Mock adatbázis"""
    return MagicMock()


@pytest.fixture
def sample_accommodation_row():
    """Mock szálláshely """
    mock_row = MagicMock()
    mock_row.id = 1
    mock_row.display_name = "Teszt Apartman"
    mock_row.active = True
    mock_row.vendegem_external_id = "VE123"
    mock_row.vendegem_external_ref = "REF456"
    return mock_row


@patch('app.services.accommodation_service.RoomMapping')
def test_find_mapping_config_by_accommodation_id(mock_room_mapping, mock_db):
    from app.services.accommodation_service import find_mapping_config_by_accommodation_id

    mock_mapping_1 = MagicMock()
    mock_mapping_1.id = 1
    mock_mapping_1.accommodation_id = 1

    mock_mapping_2 = MagicMock()
    mock_mapping_2.id = 2
    mock_mapping_2.accommodation_id = 1

    mock_db.query.return_value.filter.return_value.all.return_value = [
        mock_mapping_1,
        mock_mapping_2
    ]

    # a tényleges függvény meghívása
    result = find_mapping_config_by_accommodation_id(mock_db, accommodation_id=1)

    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2


@patch('app.services.accommodation_service.Accommodation')
def test_find_accommodation_by_id_success(mock_accommodation_model, mock_db, sample_accommodation_row):
    """
    Teszt: Szálláshely lekérdezése ID alapján sikeres.
    """
    from app.services.accommodation_service import find_accommodation_by_id

    # Mock query
    mock_db.query.return_value.filter.return_value.first.return_value = sample_accommodation_row

    result = find_accommodation_by_id(mock_db, accommodation_id=1)

    assert result is not None
    assert result['id'] == 1
    assert result['name'] == "Teszt Apartman"
    assert result['active'] is True


@patch('app.services.accommodation_service.Accommodation')
def test_find_accommodation_by_id_not_found(mock_accommodation_model, mock_db):
    """
    Teszt: Szálláshely nem található.
    """
    from app.services.accommodation_service import find_accommodation_by_id

    mock_db.query.return_value.filter.return_value.first.return_value = None

    result = find_accommodation_by_id(mock_db, accommodation_id=999)

    assert result is None


def test_find_accommodation_by_id_response_format(sample_accommodation_row):
    """
    Teszt: Válasz formázó függvény.
    """
    from app.services.accommodation_service import find_accommodation_by_id_response_format

    result = find_accommodation_by_id_response_format(sample_accommodation_row)

    assert isinstance(result, dict)
    assert result['id'] == 1
    assert result['name'] == "Teszt Apartman"
    assert 'active' in result
    assert 'vendegem_external_id' in result


@patch('app.services.accommodation_service.SyncHistory')
def test_accommodation_sync_histories(mock_sync_history, mock_db):
    """
    Teszt: Sync history lekérdezése.
    """
    from app.services.accommodation_service import accommodation_sync_histories

    mock_history_1 = MagicMock()
    mock_history_1.id = 1

    mock_history_2 = MagicMock()
    mock_history_2.id = 2

    mock_db.query.return_value.outerjoin.return_value.filter.return_value.all.return_value = [
        mock_history_1,
        mock_history_2
    ]

    result = accommodation_sync_histories(mock_db, accommodation_id=1)

    assert len(result) == 2


@patch('app.services.accommodation_service.func')
@patch('app.services.accommodation_service.UserAccommodation')
def test_number_of_accommodation_by_user_id(mock_user_accommodation, mock_func, mock_db):
    """
    Teszt: Felhasználó szálláshelyeinek száma.
    """
    from app.services.accommodation_service import number_of_accommodation_by_user_id

    mock_db.query.return_value.filter.return_value.scalar.return_value = 3

    result = number_of_accommodation_by_user_id(mock_db, user_id=1)

    assert result == 3


@patch('app.services.accommodation_service.Accommodation')
def test_accommodation_by_id_found(mock_accommodation_model, mock_db):
    """
    Teszt: Szálláshely lekérdezése ID alapján (exception-nel) - találat.
    """
    from app.services.accommodation_service import accommodation_by_id

    mock_accommodation = MagicMock()
    mock_accommodation.id = 1
    mock_accommodation.display_name = "Teszt Apartman"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_accommodation

    result = accommodation_by_id(accommodation_id=1, db=mock_db)

    assert result.id == 1
    assert result.display_name == "Teszt Apartman"


@patch('app.services.accommodation_service.Accommodation')
def test_accommodation_by_id_not_found_raises_exception(mock_accommodation_model, mock_db):
    """
    Teszt: Szálláshely nem található - HTTPException dobása.
    """
    from app.services.accommodation_service import accommodation_by_id

    mock_db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        accommodation_by_id(accommodation_id=999, db=mock_db)

    assert exc_info.value.status_code == 404
    assert "not exists" in str(exc_info.value.detail).lower()


@patch('app.services.accommodation_service.datetime')
@patch('app.services.accommodation_service.UserAccommodation')
@patch('app.services.accommodation_service.Address')
@patch('app.services.accommodation_service.Accommodation')
@patch('app.services.accommodation_service.USER_NAME', 'user_name')
def test_create_new_accommodation_success(mock_accommodation_model,
                                          mock_address_model,
                                          mock_user_accommodation_model,
                                          mock_datetime,
                                          mock_db
                                          ):
    """
    Teszt: Új szálláshely létrehozása sikeres.
    """
    from app.services.accommodation_service import create_new_accommodation

    # Mock request
    mock_request = MagicMock()
    mock_request.name = "Új Szálláshely"
    mock_request.ntak_no = "NTAK123456"
    mock_request.szallas_hu_id = "SH789"
    mock_request.vendegem_id = "VE999"
    mock_request.vendegem_ref = "REF999"
    mock_request.contact_name = "Kovács János"
    mock_request.contact_email = "kovacs@example.com"
    mock_request.contact_phone = "+36301234567"
    mock_request.user_id = 1
    mock_request.address = None

    logged_user = {'user_name': 'test_user', 'user_id': 1}

    mock_datetime.now.return_value = datetime(2025, 12, 11, 10, 0, 0)
    mock_db.query.return_value.filter.return_value.first.return_value = None

    mock_new_accommodation = MagicMock()
    mock_new_accommodation.id = 100
    mock_accommodation_model.return_value = mock_new_accommodation

    def refresh_side_effect(obj):
        obj.id = 100

    mock_db.refresh.side_effect = refresh_side_effect

    result = create_new_accommodation(
        request=mock_request,
        logged_user=logged_user,
        db=mock_db
    )

    assert result is not None
    assert 'id' in result
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@patch('app.services.accommodation_service.Accommodation')
@patch('app.services.accommodation_service.USER_NAME', 'user_name')
def test_create_new_accommodation_duplicate_ntak_raises_conflict(
        mock_accommodation_model,
        mock_db
):
    """
    Teszt: Duplikált NTAK szám - 409 Conflict.
    """
    from app.services.accommodation_service import create_new_accommodation

    mock_request = MagicMock()
    mock_request.ntak_no = "NTAK123456"
    mock_request.name = "Új Szálláshely"
    mock_request.szallas_hu_id = "SH789"

    logged_user = {'user_name': 'test_user'}

    existing = MagicMock()
    existing.reg_number = "NTAK123456"
    mock_db.query.return_value.filter.return_value.first.return_value = existing

    with pytest.raises(HTTPException) as exc_info:
        create_new_accommodation(
            request=mock_request,
            logged_user=logged_user,
            db=mock_db
        )

    assert exc_info.value.status_code == 409
    assert "already registered" in str(exc_info.value.detail).lower()
