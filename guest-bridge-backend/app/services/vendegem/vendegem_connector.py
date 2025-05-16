from datetime import datetime, timedelta
import requests
import re
from colorama import Fore, Style

from app.services.szallas_hu.constatnt import DEFAULT_DAY_DELAY
from app.services.szallas_hu.szallas_hu_connector import Reservation
from app.services.vendegem.helper import DATE_FORMAT, base_url, default_headers, auth_url, new_reservation, \
    vendegem_hun_id, vendegem_reservation_mode, vendegem_reservation_type, vendegem_guest_status, reservations_url, \
    accommodation_url, Accommodation, my_rooms_url


class Vendegem:

    def __init__(self, user: str, password: str):
        self.session = self.__setup_session(user, password)
        self.accommodation = self.my_accommodation()

    def __setup_session(self, user: str, password: str):
        with requests.Session() as s:
            self.__authentication(s, user, password)

            return s

    def reservation_id_from_customer(self, name: str):
        match = re.search(r'\[(\d+)\]', name)
        if match:
            return int(match.group(1))
        else:
            return None

    def __booking_list_payload(self, property_id, to_date=None, from_date=None):
        if to_date is None:
            to_date = datetime.now() + timedelta(days=DEFAULT_DAY_DELAY)
        if from_date is None:
            from_date = datetime.now()
        return {
            'szallashelyKulsoId': property_id,
            'lapozas': {
                'oldalSzam': 0, 'oldalMeret': 200
            },
            'szures': {
                'tavozasDatumaStart': from_date.strftime(DATE_FORMAT), 'erkezesDatumaEnd': to_date.strftime(DATE_FORMAT)
            }
        }

    def __authentication(self, session: requests.Session, user: str, password: str, account_type='SZALLASHELY'):
        auth_response = session.post(
            url=base_url + auth_url,
            json={
                'email': user,
                'password': password,
                'accountType': account_type
            },
            headers=default_headers
        )
        print(auth_response)

    def create_reservation(self, payload: Reservation):

        print(f"Reservation = [{payload.guest_name}] sync to Vendégem")
        data = self.__create_reservation_request_payload(payload)
        print(data)

        response = self.session.post(
            url=base_url + new_reservation,
            json=self.__create_reservation_request_payload(payload),
            headers={
                'Content-Type': 'application/json',
                'Content-Length': str(len(data))
            }
        )

        if response.status_code == 200:
            print(
                f"{Fore.GREEN} Reservation = [{payload.guest_name}] sync to Vendégem ~~ SUCCESSFULL {Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED} Reservation = [{payload.guest_name}] sync to Vendégem ~~ FAILED  -- RESPONSE: {response.text}{Style.RESET_ALL}")

    def __create_reservation_request_payload(self, reservation: Reservation):
        data = {
            'szallashelyKulsoId': self.accommodation.id,
            'megrendeloNev': reservation.guest_name,
            'megrendeloEmailCim': reservation.guest_email,
            'megrendeloTelefonSzam': reservation.guest_phone,
            'megrendeloAllampolgarsag': {
                'kulsoId': vendegem_hun_id
            },
            'vendegekSzama': int(reservation.guest_count),
            'foglalasMod': vendegem_reservation_mode,
            'piaciSzegmens': vendegem_reservation_type,
            'foglalasEgysegek': []
        }

        for room_number, price in reservation.rooms.items():
            room_price = self.__room_price(reservation)
            data['foglalasEgysegek'].append(
                {
                    'allapot': vendegem_guest_status,
                    'erkezesDatum': reservation.check_in,
                    'utazasDatum': reservation.check_out,
                    'lakoegysegDto': {
                        'szallashelyKulsoId': self.accommodation.id,
                        'kulsoId': self.accommodation.find_room_id_by_szallas_hu_name(room_number)['id']
                    },
                    'ejszakaAra': room_price
                }
            )
        return data

    def __room_price(self, reservation: Reservation) -> float:
        start_date = datetime.strptime(reservation.check_in, DATE_FORMAT)
        end_date = datetime.strptime(reservation.check_out, DATE_FORMAT)

        return (float(reservation.full_price) / (end_date - start_date).days) / int(reservation.room_count)

    def reservations(self, from_date=None, to_date=None):
        response = self.session.post(
            url=base_url + reservations_url,
            json=self.__booking_list_payload(
                property_id=self.accommodation.id,
                from_date=from_date,
                to_date=to_date
            )
        )
        reservations = response.json()['content']
        print(reservations)
        return reservations

    def reservation_by_id(self, szallasHuId: int):
        for r in self.reservations():
            if self.reservation_id_from_customer(r['foglaloNev']) == szallasHuId:
                return r
        return None

    def delete_reservation_by_id(self, reservation_id: str):
        response = self.session.delete(
            url=base_url + reservations_url + "/" + reservation_id,
            headers=default_headers
        )
        if response.status_code == 200:
            print(
                f"{Fore.GREEN} Reservation = [reservation_id] deleted SUCCESSFULLY form Vendégem {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} Reservation = [reservation_id] deleted FAILED form Vendégem {Style.RESET_ALL}")

    # úgy kell módosítani, hogy a szállás.hu-hoz tarotozó vendégemet nézze csak -- erre kell egy db mapping
    def my_accommodation(self):
        response = self.session.get(
            url=base_url + accommodation_url,
            headers=default_headers
        )
        available_accommodations = response.json()
        # TODO: itt minden olyan szálláshelyet látok, amihez hozzárendeltek
        # itt kell majd
        accommodation_json = response.json()[0]
        accommodation = Accommodation(
            accommodation_id=accommodation_json['kulsoId'],
            szId=accommodation_json['szolgaltatoKulsoId']
        )

        self.my_rooms(accommodation)
        return accommodation

    def my_rooms(self, accommodation: Accommodation):
        response = self.session.get(
            url=base_url + my_rooms_url + "/" + accommodation.id,
            headers=default_headers
        )
        rooms = [
            {"name": item["kod"], "id": item["kulsoId"], "max_number_of_guest": item["ferohely"]}
            for item in response.json()
        ]
        accommodation.rooms = rooms

    def visible_accommodations(self):
        response = self.session.get(
            url=base_url + accommodation_url,
            headers=default_headers
        )
        resp = response.json()
        print(resp)

        return resp

    def rooms_by_id(self, external_id: str):
        response = self.session.get(
            url=base_url + my_rooms_url + "/" + external_id,
            headers=default_headers
        )
        # print(response.json())
        rooms = [
            {
                "name": item["kod"],
                "id": item["kulsoId"],
                "max_number_of_guest": item["ferohely"]
            }
            for item in response.json()
        ]
        # print(rooms)
        return rooms
