import re
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from playwright.sync_api import Page

from app.services.szallas_hu.constatnt import ALREADY_ARRIVED, BASE_SZALLAS_HU_URL, Keys, DEFAULT_DAY_DELAY
from app.services.szallas_hu.reservation import Reservation

RESERVATION_URL = '/reservations/refresh-list'
js_date_picker_trigger = """(data) => {
                      const element = document.querySelector(data.start_selector);
                      if (element) {
                          element.value = data.start_value;
                      }
                      const end_element = document.querySelector(data.end_selector);
                      if (end_element) {
                          end_element.value = data.end_value;
                          end_element.dispatchEvent(new Event('change', { bubbles: true }));
                      }
                  }"""


def collect_reservations(page: Page, accommodation_ext_id: str,
                         from_date: datetime, to_date: datetime) -> list[Reservation]:
    url_pattern = re.compile(r'/reservations/refresh-list')

    if from_date is None:
        from_date = datetime.now()
    if to_date is None:
        to_date = from_date + timedelta(days=DEFAULT_DAY_DELAY)

    page.evaluate(js_date_picker_trigger, {
        'start_selector': 'div.table-datepicker[data-column-name="stayInterval"] input[type="hidden"].start-date-holder',
        'start_value': from_date.strftime('%Y-%m-%d'),
        'end_selector': 'div.table-datepicker[data-column-name="stayInterval"] input[type="hidden"].end-date-holder',
        'end_value': to_date.strftime('%Y-%m-%d')
    })

    with page.expect_response(url_pattern) as response_info:
        page.locator('select[name="DataTables_Table_0_length"]').select_option(label='100')

    response = response_info.value

    if response and response.ok:
        try:
            data = response.json()['data']
            print("✅ Sikeresen kinyert adatok (JSON):")

            sorted_data = sorted(
                list(filter(lambda r: r['formattedStatus'] != ALREADY_ARRIVED, data))
                , key=lambda x: datetime.strptime(x['checkIn'], "%Y-%m-%d")
            )
            # test miatt:
            sorted_data = data
            return reservation_details(page, accommodation_ext_id, sorted_data)
        except Exception as e:
            print(f"❌ Hiba: A válasz nem JSON formátumú. {e}")
    else:
        print(f"❌ Hiba a kérésnél: Válasz státuszkód: {response.status if response else 'Nincs válasz'}")


def reservation_details(page: Page, accommodation_ext_id: str, sorted_data) -> list[Reservation]:
    _reservations = []
    for data in sorted_data:
        res = Reservation(data)
        data_from_rows = reservation_detail_id(page, accommodation_ext_id, data['reservationId'])
        if data_from_rows is None:
            print(
                f"A következő foglalás nem lett szinkronizálva a Vendégembe -  {data['reservationId']}")
            continue

        res.guest_email = data_from_rows[Keys.EMAIL.value]
        rooms = data_from_rows['Szobák'].split(")")
        for room in rooms:
            if '(' in room:
                rr = room.split("(")
                res.add_room(rr[0], rr[1])

        _reservations.append(res)

    return _reservations


def reservation_detail_id(page: Page, accommodation_ext_id: str, reservation_id: str):
    full_detail_url = BASE_SZALLAS_HU_URL + f'/{accommodation_ext_id}/reservation/details?id={reservation_id}'
    try:
        page.goto(full_detail_url, timeout=30000)
        critical_selector = 'div.hotel-services'
        page.wait_for_selector(critical_selector, state='attached', timeout=10000)

    except Exception as e:
        print(f"❌ HIBA a foglalás részletek betöltésekor {reservation_id}: {e}")

    soup = BeautifulSoup(page.content(), 'html.parser')
    customer_data_div = soup.find('div', class_='hotel-services')

    reservation_data = {}
    __parse_rows(
        customer_data_div.find('div', id='guestDetails'),
        reservation_data
    )
    __parse_rows(
        customer_data_div.find('div', id='reservationDetails').find(class_='description-list'),
        reservation_data
    )
    payment_details = customer_data_div.find('div', id='paymentDetails')
    if payment_details:
        __parse_rows(
            payment_details.find(class_='description-list'),
            reservation_data
        )
    return reservation_data


def __parse_rows(html, data=None):
    if data is None:
        data = {}
    rows = html.find_all(class_='row')
    for row in rows:
        title = row.find(class_='title').get_text(strip=True)
        description = row.find(class_='description').get_text(strip=True)
        data[title.replace(":", "")] = description
