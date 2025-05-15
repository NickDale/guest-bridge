from datetime import datetime, timedelta
from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
import re

from app.services.szallas_hu.constatnt import DEFAULT_DAY_DELAY, base_url, reservation_detail_url, Keys, \
    ALREADY_ARRIVED, login_url


class Reservation:

    def __init__(self, reservation_data: dict):
        self.guest_name = reservation_data['guestFullName'] + ' [' + str(reservation_data['reservationId']) + ']'
        self.guest_count = reservation_data['guestCount']
        self._set_phone_number(reservation_data['guestPhone'])

        self.guest_email = None
        self.rooms = {}
        self.room_count = reservation_data['roomCount']
        self.full_price = reservation_data['price']
        self.check_in = reservation_data['checkIn']
        self.check_out = reservation_data['checkOut']
        self.prepaid_amount = reservation_data['onlineGuestPaymentAmount']

    def add_room(self, room_name: str, price):
        self.rooms[room_name] = price

    def _set_phone_number(self, phoneNumber):
        if phoneNumber:
            if phoneNumber.startswith('06'):
                self.guest_phone = phoneNumber.replace('06', '+36')
            else:
                self.guest_phone = phoneNumber


class SzallasHu:

    def __init__(self, user: str, password: str):
        self.session = self.__setup_session(user, password)

    def __setup_session(self, user: str, password: str):
        with requests.Session() as s:
            self.user_id = self.__authentication(s, user, password)

            return s

    def __authentication(self, session: requests.Session, user: str, password: str):
        response = session.post(
            login_url,
            {
                'email': user,
                'password': password
            }
        )
        bs = BeautifulSoup(response.text, 'html.parser')
        return re.findall(r'\d+', bs.find('base').get('href'))[0]

    def active_reservations(self, from_date=None, to_date=None):
        return self.reservations(
            reservation_url_with_filter_values=reservation_url(self.user_id, from_date=from_date, to_date=to_date)
        )

    def deleted_reservations(self, from_date=None, to_date=None):
        deleted_reservations = self.session.get(
            deleted_reservation_url(
                self.user_id,
                from_date=from_date,
                to_date=to_date
            )
        ).json()['data']

        _deleted_reservation_ids = []
        for data in deleted_reservations:
            _deleted_reservation_ids.append(data['reservationId'])

        return _deleted_reservation_ids

    def reservations(self, reservation_url_with_filter_values: str):
        reservations = self.session.get(
            reservation_url_with_filter_values
        ).json()['data']

        sorted_data = sorted(
            list(filter(lambda r: r['formattedStatus'] != ALREADY_ARRIVED, reservations))
            , key=lambda x: datetime.strptime(x['checkIn'], "%Y-%m-%d")
        )
        _reservations = []
        for data in sorted_data:
            res = Reservation(data)
            data_from_rows = self.reservation_detail(data['reservationId'])
            if data_from_rows is None:
                print(
                    f"{Fore.RED}A következő foglalás nem lett szinkronizálva a Vendégembe -  {data['reservationId']}{Style.RESET_ALL}")
                continue

            res.guest_email = data_from_rows[Keys.EMAIL.value]
            rooms = data_from_rows['Szobák'].split(")")
            for room in rooms:
                if '(' in room:
                    rr = room.split("(")
                    res.add_room(rr[0], rr[1])

            _reservations.append(res)

        return _reservations

    def __parse_rows(self, html, data=None):
        if data is None:
            data = {}
        rows = html.find_all(class_='row')
        for row in rows:
            title = row.find(class_='title').get_text(strip=True)
            description = row.find(class_='description').get_text(strip=True)
            data[title.replace(":", "")] = description

    def reservation_detail(self, reservation_id):
        resp = self.session.get(base_url + '/' + self.user_id + reservation_detail_url + str(reservation_id))
        soup = BeautifulSoup(resp.text, 'html.parser')
        customer_data_div = soup.find('div', class_='hotel-services')

        reservation_data = {}

        self.__parse_rows(
            customer_data_div.find('div', id='guestDetails'),
            reservation_data
        )
        self.__parse_rows(
            customer_data_div.find('div', id='reservationDetails').find(class_='description-list'),
            reservation_data
        )
        payment_details = customer_data_div.find('div', id='paymentDetails')
        if payment_details:
            self.__parse_rows(
                payment_details.find(class_='description-list'),
                reservation_data
            )
        return reservation_data


def reservation_url(user_id: str, from_date, to_date):
    if from_date is None:
        from_date = datetime.now()
    if to_date is None:
        to_date = from_date + timedelta(days=DEFAULT_DAY_DELAY)
    return 'https://admin.szallas.hu/' + user_id + \
        '/reservations/refresh-list?draw=13&columns%5B0%5D%5Bdata%5D=reservationId&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true' \
        '&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=guestFullName' \
        '&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=' \
        '&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=guestPhone&columns%5B2%5D%5Bname%5D=' \
        '&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false' \
        '&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=guestCount' \
        '&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true' \
        '&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=roomCount' \
        '&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=stayInterval&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=%5B%22' \
        + from_date.strftime('%Y-%m-%d') + '%22%2C%22' + to_date.strftime('%Y-%m-%d') + \
        '%22%5D&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=formattedPrice&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true' \
        '&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=loyaltyCoins' \
        '&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=' \
        '&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=finalPrice&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true' \
        '&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=amount' \
        '&columns%5B9%5D%5Bname%5D=' \
        '&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false' \
        '&columns%5B10%5D%5Bdata%5D=onlinePrepaymentDeadline&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=false' \
        '&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=guaranteeType&columns%5B11%5D%5Bname%5D=' \
        '&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=submitDate&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true' \
        '&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=status' \
        '&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true' \
        '&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=%5B%22ACTIVE_NO_PREPAYMENT%22%2C%22ACTIVE_PAID%22%5D&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=true&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=price' \
        '&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=true&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B16%5D%5Bdata%5D=checkIn&columns%5B16%5D%5Bname%5D=&columns%5B16%5D%5Bsearchable%5D=true&columns%5B16%5D%5Borderable%5D=true&columns%5B16%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B16%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=12&order%5B0%5D%5Bdir%5D=asc&start=0&length=100&search%5Bvalue%5D=&search%5Bregex%5D=false&interval=all&_=1689611514860'


def deleted_reservation_url(user_id: str, from_date, to_date):
    if from_date is None:
        from_date = datetime.now()
    if to_date is None:
        to_date = from_date + timedelta(days=DEFAULT_DAY_DELAY)
    return 'https://admin.szallas.hu/' + user_id + \
        '/reservations/refresh-list?draw=13&columns%5B0%5D%5Bdata%5D=reservationId&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true' \
        '&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=guestFullName' \
        '&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=' \
        '&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=guestPhone&columns%5B2%5D%5Bname%5D=' \
        '&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=false' \
        '&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=guestCount' \
        '&columns%5B3%5D%5Bname%5D=&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true' \
        '&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=roomCount' \
        '&columns%5B4%5D%5Bname%5D=&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=stayInterval&columns%5B5%5D%5Bname%5D=&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=%5B%22' \
        + from_date.strftime('%Y-%m-%d') + '%22%2C%22' + to_date.strftime('%Y-%m-%d') + \
        '%22%5D&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=formattedPrice&columns%5B6%5D%5Bname%5D=&columns%5B6%5D%5Bsearchable%5D=true' \
        '&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=loyaltyCoins' \
        '&columns%5B7%5D%5Bname%5D=&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=false&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=' \
        '&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=finalPrice&columns%5B8%5D%5Bname%5D=&columns%5B8%5D%5Bsearchable%5D=true' \
        '&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=amount' \
        '&columns%5B9%5D%5Bname%5D=' \
        '&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=false&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false' \
        '&columns%5B10%5D%5Bdata%5D=onlinePrepaymentDeadline&columns%5B10%5D%5Bname%5D=&columns%5B10%5D%5Bsearchable%5D=true&columns%5B10%5D%5Borderable%5D=false' \
        '&columns%5B10%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B10%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B11%5D%5Bdata%5D=guaranteeType&columns%5B11%5D%5Bname%5D=' \
        '&columns%5B11%5D%5Bsearchable%5D=true&columns%5B11%5D%5Borderable%5D=true&columns%5B11%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B11%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B12%5D%5Bdata%5D=submitDate&columns%5B12%5D%5Bname%5D=&columns%5B12%5D%5Bsearchable%5D=true' \
        '&columns%5B12%5D%5Borderable%5D=true&columns%5B12%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B12%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B13%5D%5Bdata%5D=status' \
        '&columns%5B13%5D%5Bname%5D=&columns%5B13%5D%5Bsearchable%5D=true&columns%5B13%5D%5Borderable%5D=true' \
        '&columns%5B13%5D%5Bsearch%5D%5Bvalue%5D=%5B%22GUEST_CANCELED%22%2C%22FAILED%22%5D&columns%5B13%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B14%5D%5Bdata%5D=14&columns%5B14%5D%5Bname%5D=&columns%5B14%5D%5Bsearchable%5D=true&columns%5B14%5D%5Borderable%5D=true&columns%5B14%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B14%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B15%5D%5Bdata%5D=price' \
        '&columns%5B15%5D%5Bname%5D=&columns%5B15%5D%5Bsearchable%5D=true&columns%5B15%5D%5Borderable%5D=true&columns%5B15%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B15%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B16%5D%5Bdata%5D=checkIn&columns%5B16%5D%5Bname%5D=&columns%5B16%5D%5Bsearchable%5D=true&columns%5B16%5D%5Borderable%5D=true&columns%5B16%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B16%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=12&order%5B0%5D%5Bdir%5D=asc&start=0&length=100&search%5Bvalue%5D=&search%5Bregex%5D=false&interval=all&_=1689611514860'