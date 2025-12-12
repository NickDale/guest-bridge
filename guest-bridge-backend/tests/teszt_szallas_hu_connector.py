from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from app.services.szallas_hu.reservation import Reservation
from app.services.szallas_hu.szallas_hu_connection import (
    __parse_rows,
    reservation_details,
    reservation_detail_id
)

# ============================================================================
# MOCK HTML TEMPLATES
# ============================================================================

MOCK_GUEST_DETAILS_HTML = """
<div id="guestDetails">
    <div class="row">
        <div class="title">Név:</div>
        <div class="description">Kovács János</div>
    </div>
    <div class="row">
        <div class="title">E-mail:</div>
        <div class="description">kovacs.janos@example.com</div>
    </div>
    <div class="row">
        <div class="title">Telefon:</div>
        <div class="description">+36301234567</div>
    </div>
</div>
"""

MOCK_RESERVATION_DETAILS_HTML = """
<div id="reservationDetails">
    <div class="description-list">
        <div class="row">
            <div class="title">Szobák:</div>
            <div class="description">Deluxe Szoba (15000)Standard Szoba (10000)</div>
        </div>
        <div class="row">
            <div class="title">Érkezés:</div>
            <div class="description">2025-12-15</div>
        </div>
        <div class="row">
            <div class="title">Távozás:</div>
            <div class="description">2025-12-18</div>
        </div>
    </div>
</div>
"""

MOCK_PAYMENT_DETAILS_HTML = """
<div id="paymentDetails">
    <div class="description-list">
        <div class="row">
            <div class="title">Fizetési mód:</div>
            <div class="description">Bankkártya</div>
        </div>
        <div class="row">
            <div class="title">Előleg:</div>
            <div class="description">15000 Ft</div>
        </div>
    </div>
</div>
"""

MOCK_FULL_PAGE_HTML = f"""
<html>
<body>
    <div class="hotel-services">
        {MOCK_GUEST_DETAILS_HTML}
        {MOCK_RESERVATION_DETAILS_HTML}
        {MOCK_PAYMENT_DETAILS_HTML}
    </div>
</body>
</html>
"""


def test_parse_rows_with_guest_details():
    soup = BeautifulSoup(MOCK_GUEST_DETAILS_HTML, 'html.parser')
    guest_div = soup.find('div', id='guestDetails')

    data = {}
    __parse_rows(guest_div, data)

    assert 'Név' in data
    assert data['Név'] == 'Kovács János'

    assert 'E-mail' in data
    assert data['E-mail'] == 'kovacs.janos@example.com'

    assert 'Telefon' in data
    assert data['Telefon'] == '+36301234567'


def test_parse_rows_with_reservation_details():
    """
    Teszt: Foglalás részletek parseolása.
    """
    soup = BeautifulSoup(MOCK_RESERVATION_DETAILS_HTML, 'html.parser')
    reservation_div = soup.find('div', id='reservationDetails')
    description_list = reservation_div.find(class_='description-list')

    data = {}
    __parse_rows(description_list, data)

    assert 'Szobák' in data
    assert 'Deluxe Szoba' in data['Szobák']
    assert '15000' in data['Szobák']

    assert 'Érkezés' in data
    assert data['Érkezés'] == '2025-12-15'

    assert 'Távozás' in data
    assert data['Távozás'] == '2025-12-18'


def test_parse_rows_with_payment_details():
    """
    Teszt: Fizetési adatok parseolása.
    """
    soup = BeautifulSoup(MOCK_PAYMENT_DETAILS_HTML, 'html.parser')
    payment_div = soup.find('div', id='paymentDetails')
    description_list = payment_div.find(class_='description-list')

    data = {}
    __parse_rows(description_list, data)

    assert 'Fizetési mód' in data
    assert data['Fizetési mód'] == 'Bankkártya'

    assert 'Előleg' in data
    assert data['Előleg'] == '15000 Ft'


def test_parse_rows_removes_colons_from_titles():
    """
    Teszt: A title-ből eltávolítja a kettőspontot.

    HTML: "Név:" -> dict key: "Név"
    """
    html = """
    <div>
        <div class="row">
            <div class="title">Teszt Cím:</div>
            <div class="description">Teszt Érték</div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    __parse_rows(soup, data)

    assert 'Teszt Cím' in data
    assert 'Teszt Cím:' not in data


def test_parse_rows_with_empty_description():
    """
    Teszt: Üres description kezelése.
    """
    html = """
    <div>
        <div class="row">
            <div class="title">Üres mező:</div>
            <div class="description"></div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    __parse_rows(soup, data)

    assert 'Üres mező' in data
    assert data['Üres mező'] == ''


def test_parse_rows_with_whitespace():
    html = """
    <div>
        <div class="row">
            <div class="title">  
                Címke szóközökkel  
            </div>
            <div class="description">
                Érték
                több sorban
            </div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    __parse_rows(soup, data)

    assert 'Címke szóközökkel' in data
    # A strip=True eltávolítja a felesleges szóközöket
    assert data['Címke szóközökkel'] == 'Érték\nmehr sorban'


def test_parse_rows_with_multiple_rows():
    """
    Teszt: Több row egymás után.
    """
    html = """
    <div>
        <div class="row">
            <div class="title">Első:</div>
            <div class="description">Érték 1</div>
        </div>
        <div class="row">
            <div class="title">Második:</div>
            <div class="description">Érték 2</div>
        </div>
        <div class="row">
            <div class="title">Harmadik:</div>
            <div class="description">Érték 3</div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    __parse_rows(soup, data)

    assert len(data) == 3
    assert data['Első'] == 'Érték 1'
    assert data['Második'] == 'Érték 2'
    assert data['Harmadik'] == 'Érték 3'


def test_parse_rows_with_special_characters():
    """
    Teszt: Különleges karakterek (ékezetek, szimbólumok) kezelése.
    """
    html = """
    <div>
        <div class="row">
            <div class="title">Ár (Ft):</div>
            <div class="description">15 000 Ft / éjszaka</div>
        </div>
        <div class="row">
            <div class="title">E-mail cím:</div>
            <div class="description">teszt@példa.hu</div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    __parse_rows(soup, data)

    assert 'Ár (Ft)' in data
    assert '15 000' in data['Ár (Ft)']

    assert 'E-mail cím' in data
    assert 'teszt@példa.hu' == data['E-mail cím']


@patch('app.services.szallas_hu.collector.reservation_detail_id')
def test_reservation_details_processes_sorted_data(mock_reservation_detail_id):
    mock_page = MagicMock()
    accommodation_ext_id = "AC001"

    sorted_data = [
        {
            'reservationId': '12345',
            'guestFullName': 'Kovács János',
            'guestCount': 2,
            'guestPhone': '+36301234567',
            'status': 'CONFIRMED',
            'roomCount': 1,
            'price': 30000,
            'checkIn': '2025-12-15',
            'checkOut': '2025-12-18',
            'onlineGuestPaymentAmount': 15000
        }
    ]

    # Mock reservation_detail_id válasza
    mock_reservation_detail_id.return_value = {
        'E-mail': 'kovacs@example.com',
        'Szobák': 'Deluxe Szoba (15000)'
    }

    # Függvény hívása
    reservations = reservation_details(mock_page, accommodation_ext_id, sorted_data)

    # Ellenőrzések
    assert len(reservations) == 1
    assert isinstance(reservations[0], Reservation)
    assert reservations[0].guest_email == 'kovacs@example.com'
    assert 'Deluxe Szoba' in reservations[0].rooms


@patch('app.services.szallas_hu.collector.reservation_detail_id')
def test_reservation_details_parses_multiple_rooms(mock_reservation_detail_id):
    """
    Teszt: Több szoba parseolása egy foglalásból.

    Szobák formátum: "Deluxe (15000)Standard (10000)Suite (25000)"
    """
    mock_page = MagicMock()

    sorted_data = [{
        'reservationId': '12345',
        'guestFullName': 'Nagy Péter',
        'guestCount': 4,
        'guestPhone': '+36301111111',
        'status': 'CONFIRMED',
        'roomCount': 3,
        'price': 50000,
        'checkIn': '2025-12-20',
        'checkOut': '2025-12-23',
        'onlineGuestPaymentAmount': 25000
    }]

    mock_reservation_detail_id.return_value = {
        'E-mail': 'nagy@example.com',
        'Szobák': 'Deluxe Szoba (15000)Standard Szoba (10000)Suite (25000)'
    }

    reservations = reservation_details(mock_page, 'AC001', sorted_data)

    assert len(reservations[0].rooms) == 3
    assert 'Deluxe Szoba ' in reservations[0].rooms
    assert 'Standard Szoba ' in reservations[0].rooms
    assert 'Suite ' in reservations[0].rooms


@patch('app.services.szallas_hu.collector.BeautifulSoup')
def test_reservation_detail_id_successful_parsing(mock_beautifulsoup):
    """
    Teszt: reservation_detail_id sikeresen parseol egy HTML oldalt.
    """

    mock_page = MagicMock()
    mock_page.content.return_value = MOCK_FULL_PAGE_HTML

    mock_soup = BeautifulSoup(MOCK_FULL_PAGE_HTML, 'html.parser')
    mock_beautifulsoup.return_value = mock_soup

    result = reservation_detail_id(mock_page, 'AC001', 'RES123')

    assert result is not None
    assert 'Név' in result
    assert result['Név'] == 'Kovács János'
    assert 'E-mail' in result
    assert result['E-mail'] == 'kovacs.janos@example.com'
    assert 'Szobák' in result


@patch('app.services.szallas_hu.collector.BeautifulSoup')
def test_reservation_detail_id_handles_missing_payment_details(mock_beautifulsoup):
    """
    Teszt: Ha nincs payment details, akkor sem dob hibát.
    """
    # HTML payment details nélkül
    html_without_payment = """
    <html>
    <body>
        <div class="hotel-services">
            <div id="guestDetails">
                <div class="row">
                    <div class="title">Név:</div>
                    <div class="description">Test User</div>
                </div>
            </div>
            <div id="reservationDetails">
                <div class="description-list">
                    <div class="row">
                        <div class="title">Szobák:</div>
                        <div class="description">Standard (10000)</div>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    mock_page = MagicMock()
    mock_page.content.return_value = html_without_payment

    mock_soup = BeautifulSoup(html_without_payment, 'html.parser')
    mock_beautifulsoup.return_value = mock_soup

    # Ne dobjon hibát
    result = reservation_detail_id(mock_page, 'AC001', 'RES123')

    assert result is not None
    assert 'Név' in result
    # Nincs payment details, de ez nem hiba
    assert 'Fizetési mód' not in result


@patch('app.services.szallas_hu.collector.BeautifulSoup')
def test_reservation_detail_id_page_navigation(mock_beautifulsoup):
    """
    Teszt: A függvény navigál a helyes URL-re.
    """
    mock_page = MagicMock()
    mock_page.content.return_value = MOCK_FULL_PAGE_HTML

    mock_soup = BeautifulSoup(MOCK_FULL_PAGE_HTML, 'html.parser')
    mock_beautifulsoup.return_value = mock_soup

    accommodation_ext_id = 'TEST_AC'
    reservation_id = 'RES_999'

    reservation_detail_id(mock_page, accommodation_ext_id, reservation_id)

    # Ellenőrizzük, hogy a goto hívódott a helyes URL-lel
    expected_url = f'https://admin.szallas.hu/{accommodation_ext_id}/reservation/details?id={reservation_id}'
    mock_page.goto.assert_called_once()
    assert accommodation_ext_id in mock_page.goto.call_args[0][0]
    assert reservation_id in mock_page.goto.call_args[0][0]


def test_parse_rows_with_no_rows():
    """
    Teszt: Ha nincsenek row-k, üres dict-et ad vissza.
    """
    html = """
    <div class="empty-container">
        <p>Nincs adat</p>
    </div>
    """
    soup = BeautifulSoup(html, 'html.parser')

    data = {}
    __parse_rows(soup, data)

    assert len(data) == 0


@patch('app.services.szallas_hu.collector.BeautifulSoup')
@patch('app.services.szallas_hu.collector.reservation_detail_id')
def test_full_reservation_flow(mock_detail_id, mock_beautifulsoup):
    mock_page = MagicMock()

    sorted_data = [{
        'reservationId': '99999',
        'guestFullName': 'Teljes Teszt',
        'guestCount': 2,
        'guestPhone': '+36309999999',
        'status': 'CONFIRMED',
        'roomCount': 1,
        'price': 25000,
        'checkIn': '2025-12-25',
        'checkOut': '2025-12-27',
        'onlineGuestPaymentAmount': 12500
    }]

    mock_detail_id.return_value = {
        'E-mail': 'norbert@teszt.hu',
        'Szobák': 'Premium Szoba (25000)',
        'Név': 'Teljes Teszt',
        'Telefon': '+36309999999'
    }

    reservations = reservation_details(mock_page, 'AC_TEST', sorted_data)

    assert len(reservations) == 1

    res = reservations[0]
    assert res.reservation_id == '99999'
    assert res.guest_name == 'Teljes Teszt [99999]'
    assert res.guest_email == 'teljes@teszt.hu'
    assert res.guest_count == 2
    assert res.full_price == 25000
    assert 'Premium Szoba ' in res.rooms
