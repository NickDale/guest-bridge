from unittest.mock import patch

import pytest
import requests
import requests_mock

from app.services.vendegem.helper import AUTH_URL, ACCOMMODATION_URL, NEW_RESERVATION, \
    RESERVATIONS_URL, VendegemAccommodation
from app.services.vendegem.vendegem_connector import Vendegem

MOCK_BASE_URL = 'http://test_base_url'
MOCK_DATE_FORMAT = '%Y-%m-%d'
MOCK_DEFAULT_DAY_DELAY = 90

MOCK_ACCOMMODATIONS_RESPONSE = [
    {"kulsoId": "AC001", "szolgaltatoKulsoId": "S001", "nev": "Példa Apartman", "szolgaltatoNev": "Példa Szolgáltató"},
    {"kulsoId": "AC002", "szolgaltatoKulsoId": "S002", "nev": "Teszt Vendégház", "szolgaltatoNev": "Teszt Szolgáltató"},
]

MOCK_ROOMS_RESPONSE = [
    {"kod": "ST_01", "kulsoId": "R001", "ferohely": 2},
    {"kod": "AP_02", "kulsoId": "R002", "ferohely": 4},
]

MOCK_RESERVATIONS_RESPONSE = {'content': [
    {'id': 100, 'customer': 'Béla', 'erkezes': '2025-12-20'},
    {'id': 101, 'customer': 'Anna', 'erkezes': '2025-12-25'},
]}


@pytest.fixture
def mock_vendegem_client():
    adapter = requests_mock.Adapter()

    with patch('app.services.vendegem.vendegem_connector.BASE_URL', MOCK_BASE_URL), \
            patch('app.services.vendegem.vendegem_connector.DATE_FORMAT', MOCK_DATE_FORMAT), \
            patch('app.services.vendegem.vendegem_connector.DEFAULT_DAY_DELAY', MOCK_DEFAULT_DAY_DELAY), \
            patch('app.services.vendegem.helper.BASE_URL', MOCK_BASE_URL), \
            patch('app.services.szallas_hu.constatnt.DEFAULT_DAY_DELAY', MOCK_DEFAULT_DAY_DELAY):
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        adapter.register_uri('POST', MOCK_BASE_URL + AUTH_URL, json={}, status_code=200)
        adapter.register_uri('GET', MOCK_BASE_URL + ACCOMMODATION_URL,
                             json=MOCK_ACCOMMODATIONS_RESPONSE, status_code=200)

        with patch.object(Vendegem, '_Vendegem__setup_session', return_value=session):
            client = Vendegem(user='test@user.hu', password='testpassword')
            client.session = session
            client._mock_adapter = adapter

            yield client


def test_reservation_id_extraction_success(mock_vendegem_client):
    """Sikeres ID kinyerés a szögletes zárójelből."""
    extracted_id = mock_vendegem_client.reservation_id_from_customer("Kiss Gábor [987654]")
    assert extracted_id == 987654


def test_create_reservation_failure_raises_exception(mock_vendegem_client):
    error_response = {'message': 'Invalid data'}

    mock_vendegem_client._mock_adapter.register_uri(
        'POST',
        MOCK_BASE_URL + NEW_RESERVATION,
        json=error_response,
        status_code=400
    )

    payload = {'guest': 'New Guest'}

    with pytest.raises(Exception, match='Sync failed'):
        mock_vendegem_client.create_reservation(payload)


def test_list_reservations_success(mock_vendegem_client):
    """Foglalások listázása sikeresen feldolgozza a JSON választ."""
    mock_vendegem_client._mock_adapter.register_uri(
        'POST',
        MOCK_BASE_URL + RESERVATIONS_URL,
        json=MOCK_RESERVATIONS_RESPONSE,
        status_code=200
    )

    reservations = mock_vendegem_client.list_reservations(accommodation_id='AC001')

    assert len(reservations) == 2
    assert reservations[0]['customer'] == 'Béla'
    assert reservations[1]['id'] == 101


def test_delete_reservation_success(mock_vendegem_client):
    """Foglalás törlése sikeres (HTTP 200)."""
    reservation_id = "RES123"

    mock_vendegem_client._mock_adapter.register_uri(
        'DELETE',
        MOCK_BASE_URL + RESERVATIONS_URL + "/" + reservation_id,
        status_code=200
    )

    with patch('builtins.print'):
        mock_vendegem_client.delete_reservation_by_id(reservation_id)


def test_delete_reservation_failure(mock_vendegem_client):
    reservation_id = "RES123"

    mock_vendegem_client._mock_adapter.register_uri(
        'DELETE',
        MOCK_BASE_URL + RESERVATIONS_URL + "/" + reservation_id,
        status_code=404
    )

    with patch('builtins.print'):
        mock_vendegem_client.delete_reservation_by_id(reservation_id)


@patch('app.services.vendegem.vendegem_connector.Vendegem.rooms_of_accommodation')
def test_find_accommodation_by_id_success(mock_rooms_method, mock_vendegem_client):
    """Szálláshely keresése ID alapján."""
    found_ac = mock_vendegem_client.find_accommodation_by_id("AC001")

    assert found_ac is not None
    assert found_ac.name == "Példa Apartman"

    mock_rooms_method.assert_called_once()
    assert mock_rooms_method.call_args[0][0].id == "AC001"


def test_visible_accommodations_parsing(mock_vendegem_client):
    accommodations = mock_vendegem_client.visible_accommodations

    assert len(accommodations) == 2
    assert isinstance(accommodations[0], VendegemAccommodation)
    assert accommodations[0].id == "AC001"
    assert accommodations[1].name == "Teszt Vendégház"


def test_rooms_of_accommodation_parsing(mock_vendegem_client):
    """Szobák lekérdezése és a VendegemAccommodation objektum frissítése."""
    mock_ac = VendegemAccommodation(
        accommodation_id="AC001",
        szId="S001",
        name="Test",
        owner="Test"
    )

    mock_vendegem_client._mock_adapter.register_uri(
        'GET',
        f"{MOCK_BASE_URL}/lakoegysegek/AC001",
        json=MOCK_ROOMS_RESPONSE,
        status_code=200
    )

    mock_vendegem_client.rooms_of_accommodation(mock_ac)

    assert mock_ac.rooms is not None
    assert len(mock_ac.rooms) == 2
    assert mock_ac.rooms[0]['id'] == "R001"
    assert mock_ac.rooms[0]['max_number_of_guest'] == 2


def test_rooms_by_id_parsing(mock_vendegem_client):
    external_id = "AC001"

    mock_vendegem_client._mock_adapter.register_uri(
        'GET',
        f"{MOCK_BASE_URL}/lakoegysegek/{external_id}",
        json=MOCK_ROOMS_RESPONSE,
        status_code=200
    )

    rooms = mock_vendegem_client.rooms_by_id(external_id)

    assert len(rooms) == 2
    assert rooms[1]['name'] == "AP_02"
    assert rooms[1]['max_number_of_guest'] == 4
