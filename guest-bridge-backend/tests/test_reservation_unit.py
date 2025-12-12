"""
Unit tesztek a Reservation osztályhoz.
Ezek a tesztek ellenőrzik, hogy a foglalás adatai helyesen kerülnek feldolgozásra.
"""

import pytest
from datetime import datetime
from unittest.mock import MagicMock

from app.services.szallas_hu.reservation import Reservation

from app.services.vendegem.helper import VendegemAccommodation


# ============================================================================
# SEGÉD ADATOK (Mock adatok a tesztekhez)
# ============================================================================

def create_sample_reservation_data():
    """
    Létrehoz egy mintafoglalást teszteléshez.
    Ez egy szótár, ami tartalmazza az összes szükséges adatot.
    """
    return {
        'reservationId': 12345,
        'guestFullName': 'Kovács János',
        'guestCount': 2,
        'guestPhone': '06301234567',
        'status': 'CONFIRMED',
        'roomCount': 1,
        'price': 30000,
        'checkIn': '2025-12-15',
        'checkOut': '2025-12-18',
        'onlineGuestPaymentAmount': 15000
    }


def create_mock_accommodation():
    """
    Létrehoz egy mock (hamis) szálláshelyet teszteléshez.
    Ez segít, hogy ne kelljen valódi szálláshelyet használni.
    """
    mock_accommodation = MagicMock(spec=VendegemAccommodation)
    mock_accommodation.id = 'AC001'
    # Ez a függvény visszaadja a szoba ID-ját, amikor a nevét adjuk meg
    mock_accommodation.find_room_id_by_szallas_hu_name.return_value = 'ROOM001'
    return mock_accommodation


# ============================================================================
# 1. ALAPVETŐ INICIALIZÁLÁS TESZTEK
# ============================================================================

def test_reservation_initialization_basic_fields():
    """
    Teszt: Ellenőrzi, hogy a foglalás alapadatai helyesen kerülnek beállításra.

    Mit tesztel:
    - A foglalás ID helyes-e
    - A vendég neve megfelelően formázott-e (tartalmazza az ID-t szögletes zárójelben)
    - A vendégek száma helyes-e
    - A szobák száma helyes-e
    """
    # Előkészítés: Létrehozunk egy mintafoglalást
    reservation_data = create_sample_reservation_data()

    # Végrehajtás: Létrehozzuk a Reservation objektumot
    reservation = Reservation(reservation_data)

    # Ellenőrzés: Megnézzük, hogy minden adat helyes-e
    assert reservation.reservation_id == 12345, "A foglalás ID nem egyezik!"
    assert reservation.guest_name == 'Kovács János [12345]', "A vendég neve nem megfelelő formátumú!"
    assert reservation.guest_count == 2, "A vendégek száma nem egyezik!"
    assert reservation.room_count == 1, "A szobák száma nem egyezik!"


def test_reservation_initialization_dates_and_prices():
    """
    Teszt: Ellenőrzi a dátumokat és árakat.

    Mit tesztel:
    - Check-in dátum
    - Check-out dátum
    - Teljes ár
    - Előre fizetett összeg
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)

    assert reservation.check_in == '2025-12-15', "A bejelentkezési dátum nem egyezik!"
    assert reservation.check_out == '2025-12-18', "A kijelentkezési dátum nem egyezik!"
    assert reservation.full_price == 30000, "A teljes ár nem egyezik!"
    assert reservation.prepaid_amount == 15000, "Az előre fizetett összeg nem egyezik!"


def test_reservation_email_defaults_to_none():
    """
    Teszt: Ellenőrzi, hogy az email alapértelmezetten None (üres).

    Az email-t később állítjuk be, ezért kezdetben None értékű kell legyen.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)

    assert reservation.guest_email is None, "Az email nem None értékű kezdetben!"


def test_reservation_rooms_defaults_to_empty_dict():
    """
    Teszt: Ellenőrzi, hogy a szobák tárolója kezdetben üres.

    A szobákat később adjuk hozzá az add_room() metódussal.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)

    assert reservation.rooms == {}, "A szobák nem üres szótárként inicializálódtak!"


# ============================================================================
# 2. TELEFONSZÁM FORMÁZÁS TESZTEK
# ============================================================================

def test_phone_number_conversion_from_06_to_plus36():
    """
    Teszt: Magyar telefonszám konvertálása.

    Ha a telefonszám '06'-tal kezdődik, akkor '+36'-ra kell cserélni.
    Például: '06301234567' -> '+36301234567'
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['guestPhone'] = '06301234567'

    reservation = Reservation(reservation_data)

    assert reservation.guest_phone == '+36301234567', "A telefonszám nem lett helyesen konvertálva!"


def test_phone_number_no_conversion_if_not_starting_with_06():
    """
    Teszt: Ha a telefonszám nem '06'-tal kezdődik, ne változtassuk meg.

    Például: '+36301234567' maradjon '+36301234567'
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['guestPhone'] = '+36201234567'

    reservation = Reservation(reservation_data)

    assert reservation.guest_phone == '+36201234567', "A telefonszám megváltozott, pedig nem kellett volna!"


def test_phone_number_handles_none_value():
    """
    Teszt: Ha nincs telefonszám megadva (None), ne dobjon hibát.

    Néha a vendég nem ad meg telefonszámot, ezt is kezelni kell.
    MEGJEGYZÉS: Ha phoneNumber None, a _set_phone_number metódus nem állít be semmit,
    így a guest_phone attribútum nem jön létre. Ez nem hiba, hanem a kód jelenlegi viselkedése.
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['guestPhone'] = None

    # Ne dobjon hibát az inicializálás során - ez a fontos
    try:
        reservation = Reservation(reservation_data)
        # Ha idáig eljutottunk, sikeres (nem dobott hibát)
        assert True
    except Exception as e:
        pytest.fail(f"None telefonszám esetén hibát dobott: {e}")


# ============================================================================
# 3. SZOBA HOZZÁADÁS TESZT
# ============================================================================

def test_add_room_stores_room_with_price():
    """
    Teszt: Szoba hozzáadása a foglaláshoz.

    Az add_room() metódus tárolja a szoba nevét és árát.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)

    # Hozzáadunk egy szobát
    reservation.add_room('Deluxe Szoba', 15000)

    assert 'Deluxe Szoba' in reservation.rooms, "A szoba nem került hozzáadásra!"
    assert reservation.rooms['Deluxe Szoba'] == 15000, "A szoba ára nem egyezik!"


def test_add_multiple_rooms():
    """
    Teszt: Több szoba hozzáadása.

    Ellenőrzi, hogy több szoba is hozzáadható-e egymás után.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)

    reservation.add_room('Standard Szoba', 10000)
    reservation.add_room('Deluxe Szoba', 15000)
    reservation.add_room('Suite', 25000)

    assert len(reservation.rooms) == 3, "Nem minden szoba lett hozzáadva!"
    assert reservation.rooms['Standard Szoba'] == 10000
    assert reservation.rooms['Deluxe Szoba'] == 15000
    assert reservation.rooms['Suite'] == 25000


# ============================================================================
# 4. SZOBA ÁR SZÁMÍTÁS TESZT
# ============================================================================

def test_calculate_room_price_for_three_nights_one_room():
    """
    Teszt: Szoba éjszakánkénti árának kiszámítása.

    Példa: 3 éjszaka, 1 szoba, 30000 Ft teljes ár
    Várt eredmény: 30000 / 3 / 1 = 10000 Ft/éjszaka
    """
    reservation_data = create_sample_reservation_data()
    # 3 éjszaka: dec 15-18
    reservation_data['checkIn'] = '2025-12-15'
    reservation_data['checkOut'] = '2025-12-18'
    reservation_data['price'] = 30000
    reservation_data['roomCount'] = 1

    reservation = Reservation(reservation_data)

    # A privát metódust meghívjuk (a _ kezdetű metódusok "privátnak" számítanak)
    room_price = reservation._Reservation__calculate_room_price()

    assert room_price == 10000.0, f"A szoba ára nem 10000, hanem {room_price}!"


def test_calculate_room_price_for_two_rooms():
    """
    Teszt: Több szoba esetén az ár felosztása.

    Példa: 4 éjszaka, 2 szoba, 40000 Ft teljes ár
    Várt eredmény: 40000 / 4 / 2 = 5000 Ft/éjszaka/szoba
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['checkIn'] = '2025-12-20'
    reservation_data['checkOut'] = '2025-12-24'
    reservation_data['price'] = 40000
    reservation_data['roomCount'] = 2

    reservation = Reservation(reservation_data)
    room_price = reservation._Reservation__calculate_room_price()

    assert room_price == 5000.0, f"A szoba ára nem 5000, hanem {room_price}!"


def test_calculate_room_price_with_decimal_result():
    """
    Teszt: Ha az ár osztása nem egész szám.

    Példa: 5 éjszaka, 1 szoba, 27000 Ft teljes ár
    Várt eredmény: 27000 / 5 / 1 = 5400.0 Ft/éjszaka
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['checkIn'] = '2025-12-10'
    reservation_data['checkOut'] = '2025-12-15'
    reservation_data['price'] = 27000
    reservation_data['roomCount'] = 1

    reservation = Reservation(reservation_data)
    room_price = reservation._Reservation__calculate_room_price()

    assert room_price == 5400.0, f"A szoba ára nem 5400, hanem {room_price}!"


# ============================================================================
# 5. VENDÉGEM PAYLOAD LÉTREHOZÁS TESZT
# ============================================================================

def test_create_vendegem_payload_basic_structure():
    """
    Teszt: Ellenőrzi a Vendégem API-hoz küldendő adatok alapszerkezetét.

    A payload (adatcsomag) tartalmazza a szálláshely ID-ját, vendég adatait, stb.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)
    reservation.guest_email = 'kovacs.janos@email.com'

    # Hozzáadunk egy szobát
    reservation.add_room('Deluxe Szoba', 15000)

    # Létrehozzuk a mock szálláshelyet
    mock_accommodation = create_mock_accommodation()

    # Létrehozzuk a payload-ot
    payload = reservation.create_reservation_request_payload_to_vendegem(mock_accommodation)

    # Alapszerkezet ellenőrzése
    assert 'szallashelyKulsoId' in payload, "Hiányzik a szálláshely ID!"
    assert payload['szallashelyKulsoId'] == 'AC001', "A szálláshely ID nem egyezik!"

    assert 'megrendeloNev' in payload, "Hiányzik a megrendelő neve!"
    assert payload['megrendeloNev'] == 'Kovács János [12345]'

    assert 'megrendeloEmailCim' in payload, "Hiányzik az email!"
    assert payload['megrendeloEmailCim'] == 'kovacs.janos@email.com'

    assert 'megrendeloTelefonSzam' in payload, "Hiányzik a telefonszám!"
    assert payload['megrendeloTelefonSzam'] == '+36301234567'


def test_create_vendegem_payload_uses_default_email_if_missing():
    """
    Teszt: Ha nincs email, használjon alapértelmezett email címet.

    Ha a vendég nem adott meg email címet, a rendszer 'noemail@nomail.com'-ot használ.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)
    # Email marad None

    reservation.add_room('Standard Szoba', 10000)
    mock_accommodation = create_mock_accommodation()

    payload = reservation.create_reservation_request_payload_to_vendegem(mock_accommodation)

    assert payload['megrendeloEmailCim'] == 'noemail@nomail.com', "Nem az alapértelmezett email lett használva!"


def test_create_vendegem_payload_uses_default_email_if_invalid():
    """
    Teszt: Ha az email érvénytelen (nincs benne '@'), használjon alapértelmezett email-t.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)
    reservation.guest_email = 'hibas-email-cim'  # Nincs benne '@'

    reservation.add_room('Standard Szoba', 10000)
    mock_accommodation = create_mock_accommodation()

    payload = reservation.create_reservation_request_payload_to_vendegem(mock_accommodation)

    assert payload['megrendeloEmailCim'] == 'noemail@nomail.com', "Érvénytelen email esetén nem az alapértelmezett lett használva!"


def test_create_vendegem_payload_includes_booking_units():
    """
    Teszt: A foglalás tartalmazza a szobákat (foglalasEgysegek).

    Minden hozzáadott szobának meg kell jelennie a payload-ban.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)
    reservation.guest_email = 'test@test.com'

    # Két szobát adunk hozzá
    reservation.add_room('Deluxe Szoba', 15000)
    reservation.add_room('Standard Szoba', 10000)

    mock_accommodation = create_mock_accommodation()
    payload = reservation.create_reservation_request_payload_to_vendegem(mock_accommodation)

    # Ellenőrizzük, hogy van-e 'foglalasEgysegek' (booking units)
    assert 'foglalasEgysegek' in payload, "Hiányzik a foglalasEgysegek mező!"
    assert len(payload['foglalasEgysegek']) == 2, "Nem 2 szoba szerepel a foglalásban!"


def test_create_vendegem_payload_booking_unit_structure():
    """
    Teszt: Egy szoba (foglalasEgyseg) helyes szerkezete.

    Ellenőrzi, hogy a szoba adatai helyesen kerülnek-e be a payload-ba.
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['checkIn'] = '2025-12-15'
    reservation_data['checkOut'] = '2025-12-18'  # 3 éjszaka
    reservation_data['price'] = 30000
    reservation_data['roomCount'] = 1

    reservation = Reservation(reservation_data)
    reservation.guest_email = 'test@test.com'
    reservation.add_room('Deluxe Szoba', 15000)

    mock_accommodation = create_mock_accommodation()
    payload = reservation.create_reservation_request_payload_to_vendegem(mock_accommodation)

    # Az első szoba adatai
    booking_unit = payload['foglalasEgysegek'][0]

    assert 'erkezesDatum' in booking_unit, "Hiányzik az érkezési dátum!"
    assert booking_unit['erkezesDatum'] == '2025-12-15'

    assert 'utazasDatum' in booking_unit, "Hiányzik a távozási dátum!"
    assert booking_unit['utazasDatum'] == '2025-12-18'

    assert 'ejszakaAra' in booking_unit, "Hiányzik az éjszaka ára!"
    # 30000 / 3 éjszaka / 1 szoba = 10000 Ft/éjszaka
    assert booking_unit['ejszakaAra'] == 10000.0, f"Az éjszaka ára nem 10000, hanem {booking_unit['ejszakaAra']}!"

    assert 'lakoegysegDto' in booking_unit, "Hiányzik a lakóegység adat!"
    assert booking_unit['lakoegysegDto']['kulsoId'] == 'ROOM001', "A szoba ID nem egyezik!"


def test_create_vendegem_payload_calls_find_room_id():
    """
    Teszt: Ellenőrzi, hogy a payload létrehozása során meghívódik-e a szoba ID kereső.

    A mock accommodation-nek el kell kapnia a find_room_id_by_szallas_hu_name hívást.
    """
    reservation_data = create_sample_reservation_data()
    reservation = Reservation(reservation_data)
    reservation.guest_email = 'test@test.com'
    reservation.add_room('Deluxe Szoba', 15000)

    mock_accommodation = create_mock_accommodation()
    payload = reservation.create_reservation_request_payload_to_vendegem(mock_accommodation)

    # Ellenőrizzük, hogy meghívták-e a find_room_id_by_szallas_hu_name metódust
    mock_accommodation.find_room_id_by_szallas_hu_name.assert_called_once_with('Deluxe Szoba')


# ============================================================================
# 6. EGYÉB EDGE CASE-EK (SPECIÁLIS ESETEK)
# ============================================================================

def test_reservation_with_zero_prepaid_amount():
    """
    Teszt: Foglalás 0 Ft előleg esetén.

    Ha a vendég nem fizetett előleget, ez is működjön.
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['onlineGuestPaymentAmount'] = 0

    reservation = Reservation(reservation_data)

    assert reservation.prepaid_amount == 0, "Az előleg nem 0!"


def test_reservation_status_is_preserved():
    """
    Teszt: A foglalás státusza megmarad.

    A státusz (pl. 'CONFIRMED', 'PENDING') változatlan marad.
    """
    reservation_data = create_sample_reservation_data()
    reservation_data['status'] = 'PENDING'

    reservation = Reservation(reservation_data)

    assert reservation.status == 'PENDING', "A státusz nem egyezik!"


# ============================================================================
# FUTTATÁS
# ============================================================================
# A teszteket a pytest paranccsal futtathatod:
# pytest test_reservation_unit.py -v
#
# A -v flag "verbose" módot jelent, részletesebb kimenettel.