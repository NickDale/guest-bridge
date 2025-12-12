# test_vendegem_unit.py

import pytest
import requests_mock
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta

# IDE KELL A HELYES IMPORT ÚTVONAL!
# Kérem ellenőrizze, hogy a fájlneve Vendegem a vendegem_class.py-ban vagy a vendegem_connector.py-ban van!
# Feltételezzük, hogy az Ön Vendegem kódja a vendegem_class.py fájlban van
from app.services.vendegem.vendegem_class import Vendegem

# Importáljuk a segítő fájl konstansait, hogy mockolni tudjuk őket
from app.services.vendegem.helper import DATE_FORMAT, BASE_URL, AUTH_URL, ACCOMMODATION_URL, NEW_RESERVATION, \
    RESERVATIONS_URL, VendegemAccommodation
# Mockoljuk a külső konstansokat a stabil tesztelés érdekében
from app.services.szallas_hu.constatnt import DEFAULT_DAY_DELAY

# --- MOCK KONSTANSOK ÉS ADATOK ---

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
    """
    Mockolt Vendegem kliens, ami nem hív valódi API-kat.
    Patch-eli a külső URL-eket és a belső metódusokat az inicializációhoz.
    """
    with requests_mock.Mocker() as m:
        # Mockoljuk a hitelesítést (AUTH_URL)
        m.post(MOCK_BASE_URL + AUTH_URL, json={}, status_code=200)

        # Mockoljuk a visible_accommodations által hívott ACCOMMODATION_URL-t
        m.get(MOCK_BASE_URL + ACCOMMODATION_URL, json=MOCK_ACCOMMODATIONS_RESPONSE, status_code=200)

        # Mockoljuk a külső URL-eket a helper fájlban a tesztelés idejére
        with patch('app.services.vendegem.helper.BASE_URL', MOCK_BASE_URL), \
                patch('app.services.vendegem.helper.DATE_FORMAT', MOCK_DATE_FORMAT), \
                patch('app.services.szallas_hu.constatnt.DEFAULT_DAY_DELAY', MOCK_DEFAULT_DAY_DELAY), \
                patch('app.services.vendegem.vendegem_class.DEFAULT_DAY_DELAY', MOCK_DEFAULT_DAY_DELAY):
            # Mivel az __init__ meghívja a visible_accommodations-t, a fenti mockok már lefedik.
            client = Vendegem(user='test@user.hu', password='testpassword')
            client.mock_adapter = m  # Hozzáadjuk a mockert a további kérésekhez
            return client


# --- A. Tiszta Logika Tesztek (Nincs Hálózat) ---

def test_reservation_id_extraction_success(mock_vendegem_client):
    """Sikeres ID kinyerés a szögletes zárójelből."""
    client = mock_vendegem_client
    name_with_id = "Kiss Gábor [987654]"
    extracted_id = client.reservation_id_from_customer(name_with_id)
    assert extracted_id == 987654


def test_reservation_id_extraction_no_id(mock_vendegem_client):
    """Nincs ID a névben."""
    client = mock_vendegem_client
    name_without_id = "Kovács Béla"
    extracted_id = client.reservation_id_from_customer(name_without_id)
    assert extracted_id is None


def test_booking_list_payload_default_dates(mock_vendegem_client):
    """Payload ellenőrzése alapértelmezett dátumokkal."""
    client = mock_vendegem_client

    # Mockoljuk a datetime.now()-t, hogy ne függjön a futtatás idejétől
    test_now = datetime(2025, 1, 15)

    with patch('app.services.vendegem.vendegem_class.datetime') as mock_dt:
        mock_dt.now.return_value = test_now
        mock_dt.strftime = datetime.strftime  # A strftime meghagyása
        mock_dt.timedelta = timedelta  # A timedelta meghagyása

        payload = client._Vendegem__booking_list_payload(property_id='AC001')  # A belső metódus tesztelése

        expected_to_date = (test_now + timedelta(days=MOCK_DEFAULT_DAY_DELAY)).strftime(MOCK_DATE_FORMAT)

        assert payload['szallashelyKulsoId'] == 'AC001'
        assert payload['szures']['tavozasDatumaStart'] == '2025-01-15'
        assert payload['szures']['erkezesDatumaEnd'] == expected_to_date  # 90 nappal későbbi dátum


# --- B. CRUD Funkciók Tesztjei (Hálózati Mocking) ---

def test_create_reservation_success(mock_vendegem_client):
    """Foglalás létrehozása sikeres (HTTP 201)."""
    client = mock_vendegem_client

    # Mockoljuk a sikeres API választ (201 Created)
    client.mock_adapter.post(MOCK_BASE_URL + NEW_RESERVATION, status_code=201)

    payload = {'guest': 'New Guest'}

    try:
        client.create_reservation(payload)
        # Nincs exception, siker
    except Exception:
        pytest.fail("A sikeres (201) válasz hibát dobott.")


def test_create_reservation_failure_raises_exception(mock_vendegem_client):
    """Foglalás létrehozása sikertelen (HTTP 400), exception-t dob."""
    client = mock_vendegem_client

    # Mockoljuk a hibás API választ (400 Bad Request)
    error_response = {'message': 'Invalid data'}
    client.mock_adapter.post(MOCK_BASE_URL + NEW_RESERVATION, json=error_response, status_code=400)

    payload = {'guest': 'New Guest'}

    # Elvárjuk, hogy a metódus Exception-t dobjon
    with pytest.raises(Exception, match='Sync failed'):
        client.create_reservation(payload)


def test_list_reservations_success(mock_vendegem_client):
    """Foglalások listázása sikeresen feldolgozza a JSON választ."""
    client = mock_vendegem_client

    # Mockoljuk a RESERVATIONS_URL endpointot
    client.mock_adapter.post(MOCK_BASE_URL + RESERVATIONS_URL, json=MOCK_RESERVATIONS_RESPONSE, status_code=200)

    reservations = client.list_reservations(accommodation_id='AC001')

    # Ellenőrizzük a válasz feldolgozását
    assert len(reservations) == 2
    assert reservations[0]['customer'] == 'Béla'
    assert reservations[1]['id'] == 101


def test_delete_reservation_success(mock_vendegem_client):
    """Foglalás törlése sikeres (HTTP 200)."""
    client = mock_vendegem_client
    reservation_id_to_delete = "RES123"

    # Mockoljuk a sikeres törlés választ (200 OK)
    client.mock_adapter.delete(MOCK_BASE_URL + RESERVATIONS_URL + "/" + reservation_id_to_delete, status_code=200)

    try:
        client.delete_reservation_by_id(reservation_id_to_delete)
        # Nincs exception, siker
    except Exception:
        pytest.fail("A sikeres törlés (200) hibát dobott.")


def test_delete_reservation_failure(mock_vendegem_client):
    """Foglalás törlése sikertelen (HTTP 404)."""
    client = mock_vendegem_client
    reservation_id_to_delete = "RES123"

    # Mockoljuk a sikertelen törlés választ (404 Not Found)
    client.mock_adapter.delete(MOCK_BASE_URL + RESERVATIONS_URL + "/" + reservation_id_to_delete, status_code=404)

    # Bár a kód csak print-et hív, ellenőrizzük, hogy nincs-e Exception dobás
    try:
        client.delete_reservation_by_id(reservation_id_to_delete)
    except Exception:
        pytest.fail("A sikertelen törlés (404) is hibát dobott, pedig nem kellene.")


# --- C. Egyéb Metódusok Tesztjei (Szálláshely és szoba) ---

@patch('app.services.vendegem.vendegem_class.Vendegem.rooms_of_accommodation')
def test_find_accommodation_by_id_success(mock_rooms_of_accommodation, mock_vendegem_client):
    """Szálláshely keresése ID alapján, és ellenőrizzük, hogy meghívódott-e a rooms_of_accommodation."""
    client = mock_vendegem_client

    found_ac = client.find_accommodation_by_id("AC001")

    assert found_ac is not None
    assert found_ac.name == "Példa Apartman"

    # Ellenőrizzük, hogy a metódus meghívta-e a szobakereső metódust a talált accommodation objektummal
    mock_rooms_of_accommodation.assert_called_once()
    assert mock_rooms_of_accommodation.call_args[0][0].id == "AC001"


def test_find_accommodation_by_id_not_found(mock_vendegem_client):
    """Szálláshely keresése ismeretlen ID-vel."""
    client = mock_vendegem_client
    found_ac = client.find_accommodation_by_id("AC999")
    assert found_ac is None


def test_visible_accommodations_parsing(mock_vendegem_client):
    """Ellenőrizzük, hogy az inicializálás során a válasz helyesen parszolásra került-e VendegemAccommodation objektumokká."""
    client = mock_vendegem_client

    accommodations = client.visible_accommodations

    assert len(accommodations) == 2
    assert isinstance(accommodations[0], VendegemAccommodation)
    assert accommodations[0].id == "AC001"
    assert accommodations[1].name == "Teszt Vendégház"


def test_rooms_of_accommodation_parsing(mock_vendegem_client):
    """Szobák lekérdezése és a VendegemAccommodation objektum rooms attribútumának frissítése."""
    client = mock_vendegem_client

    # Mockoljuk a szobák endpointját
    mock_ac = VendegemAccommodation(accommodation_id="AC001", szId="S001", name="Test", owner="Test")
    client.mock_adapter.get(f"{MOCK_BASE_URL}/api/accommodation/myrooms/AC001", json=MOCK_ROOMS_RESPONSE,
                            status_code=200)

    client.rooms_of_accommodation(mock_ac)

    # Ellenőrizzük, hogy a rooms attribútum frissült-e
    assert mock_ac.rooms is not None
    assert len(mock_ac.rooms) == 2
    assert mock_ac.rooms[0]['id'] == "R001"
    assert mock_ac.rooms[0]['max_number_of_guest'] == 2


def test_rooms_by_id_parsing(mock_vendegem_client):
    """Szobák lekérdezése külső ID alapján és a lista visszatérése."""
    client = mock_vendegem_client

    # Mockoljuk a szobák endpointját
    external_id = "AC001"
    client.mock_adapter.get(f"{MOCK_BASE_URL}/api/accommodation/myrooms/{external_id}", json=MOCK_ROOMS_RESPONSE,
                            status_code=200)

    rooms = client.rooms_by_id(external_id)

    # Ellenőrizzük a visszatérő lista szerkezetét
    assert len(rooms) == 2
    assert rooms[1]['name'] == "AP_02"
    assert rooms[1]['max_number_of_guest'] == 4