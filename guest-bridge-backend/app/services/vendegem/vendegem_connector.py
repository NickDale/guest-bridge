import re
from datetime import datetime, timedelta

import requests
from colorama import Fore, Style

from app.services.szallas_hu.constatnt import DEFAULT_DAY_DELAY
from app.services.vendegem.helper import DATE_FORMAT, BASE_URL, DEFAULT_HEADERS, AUTH_URL, NEW_RESERVATION, \
    ACCOMMODATION_URL, VendegemAccommodation, MY_ROOMS_URL, RESERVATIONS_URL


class Vendegem:

    def __init__(self, user: str, password: str):
        self.session = self.__setup_session(user, password)
        self.visible_accommodations = self.visible_accommodations()

    def __setup_session(self, user: str, password: str):
        with requests.Session() as s:
            self.__authentication(s, user, password)

            return s

    def find_accommodation_by_id(self, vendegem_id: str):
        try:
            found_accommodation = next(
                (ac for ac in self.visible_accommodations if ac.id == vendegem_id),
                None
            )
            if found_accommodation:
                self.rooms_of_accommodation(found_accommodation)
                return found_accommodation
        except Exception as e:
            print(f"Hiba történt a keresés során: {e}")
            return None

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
            url=BASE_URL + AUTH_URL,
            json={
                'email': user,
                'password': password,
                'accountType': account_type
            },
            headers=DEFAULT_HEADERS
        )
        print(auth_response)

    def create_reservation(self, request_payload: dict):
        print(request_payload)

        response = self.session.post(
            url=BASE_URL + NEW_RESERVATION,
            json=request_payload,
            headers={
                'Content-Type': 'application/json',
                'Content-Length': str(len(request_payload))
            }
        )

        if response.status_code in [200, 201]:
            print(
                f"{Fore.GREEN} Reservation sync to Vendégem ~~ SUCCESSFULL {Style.RESET_ALL}")
        else:
            print(
                f"{Fore.RED} Reservation = sync to Vendégem ~~ FAILED  -- RESPONSE: {response.text}{Style.RESET_ALL}")

    # def create_reservation(self, accommodation: VendegemAccommodation, payload: Reservation):
    #     print(f"Reservation = [{payload.guest_name}] sync to Vendégem")
    #     data = self.__create_reservation_request_payload(payload)
    #     print(data)
    #
    #     response = self.session.post(
    #         url=BASE_URL + NEW_RESERVATION,
    #         json=self.__create_reservation_request_payload(payload),
    #         headers={
    #             'Content-Type': 'application/json',
    #             'Content-Length': str(len(data))
    #         }
    #     )
    #
    #     if response.status_code == 200:
    #         print(
    #             f"{Fore.GREEN} Reservation = [{payload.guest_name}] sync to Vendégem ~~ SUCCESSFULL {Style.RESET_ALL}")
    #     else:
    #         print(
    #             f"{Fore.RED} Reservation = [{payload.guest_name}] sync to Vendégem ~~ FAILED  -- RESPONSE: {response.text}{Style.RESET_ALL}")

    # def __create_reservation_request_payload(self, reservation: Reservation):
    #     data = {
    #         'szallashelyKulsoId': self.accommodation.id,
    #         'megrendeloNev': reservation.guest_name,
    #         'megrendeloEmailCim': reservation.guest_email,
    #         'megrendeloTelefonSzam': reservation.guest_phone,
    #         'megrendeloAllampolgarsag': {
    #             'kulsoId': VENDEGEM_HUN_ID
    #         },
    #         'vendegekSzama': int(reservation.guest_count),
    #         'foglalasMod': VENDEGEM_RESERVATION_MODE,
    #         'piaciSzegmens': VENDEGEM_RESERVATION_TYPE,
    #         'foglalasEgysegek': []
    #     }
    #
    #     for room_number, price in reservation.rooms.items():
    #         room_price = self.__room_price(reservation)
    #         data['foglalasEgysegek'].append(
    #             {
    #                 'allapot': VENDEGEM_GUEST_STATUS,
    #                 'erkezesDatum': reservation.check_in,
    #                 'utazasDatum': reservation.check_out,
    #                 'lakoegysegDto': {
    #                     'szallashelyKulsoId': self.accommodation.id,
    #                     'kulsoId': self.accommodation.find_room_id_by_szallas_hu_name(room_number)['id']
    #                 },
    #                 'ejszakaAra': room_price
    #             }
    #         )
    #     return data

    # def __room_price(self, reservation: Reservation) -> float:
    #     start_date = datetime.strptime(reservation.check_in, DATE_FORMAT)
    #     end_date = datetime.strptime(reservation.check_out, DATE_FORMAT)
    #
    #     return (float(reservation.full_price) / (end_date - start_date).days) / int(reservation.room_count)

    def list_reservations(self, accommodation_id: str, from_date=None, to_date=None):
        response = self.session.post(
            url=BASE_URL + RESERVATIONS_URL,
            json=self.__booking_list_payload(
                property_id=accommodation_id,
                from_date=from_date,
                to_date=to_date
            )
        )
        reservations = response.json()['content']
        return reservations

    # def reservation_by_id(self, szallasHuId: int):
    #     for r in self.list_reservations():
    #         if self.reservation_id_from_customer(r['foglaloNev']) == szallasHuId:
    #             return r
    #     return None

    def delete_reservation_by_id(self, reservation_id: str):
        response = self.session.delete(
            url=BASE_URL + RESERVATIONS_URL + "/" + reservation_id,
            headers=DEFAULT_HEADERS
        )
        if response.status_code == 200 or response.status_code == 204:
            print(
                f"{Fore.GREEN} Reservation = [reservation_id] deleted SUCCESSFULLY form Vendégem {Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} Reservation = [reservation_id] deleted FAILED form Vendégem {Style.RESET_ALL}")

    def visible_accommodations(self):
        response = self.session.get(
            url=BASE_URL + ACCOMMODATION_URL,
            headers=DEFAULT_HEADERS
        )
        visible_accommodations = [
            VendegemAccommodation(
                accommodation_id=ac['kulsoId'],
                szId=ac['szolgaltatoKulsoId'],
                name=ac['nev'],
                owner=ac['szolgaltatoNev']
            )
            for ac in response.json()
        ]
        return visible_accommodations

    def rooms_of_accommodation(self, accommodation: VendegemAccommodation):
        response = self.session.get(
            url=BASE_URL + MY_ROOMS_URL + "/" + accommodation.id,
            headers=DEFAULT_HEADERS
        )
        rooms = [
            {"name": item["kod"], "id": item["kulsoId"], "max_number_of_guest": item["ferohely"]}
            for item in response.json()
        ]
        accommodation.rooms = rooms

    def rooms_by_id(self, external_id: str):
        response = self.session.get(
            url=BASE_URL + MY_ROOMS_URL + "/" + external_id,
            headers=DEFAULT_HEADERS
        )
        rooms = [
            {
                "name": item["kod"],
                "id": item["kulsoId"],
                "max_number_of_guest": item["ferohely"]
            }
            for item in response.json()
        ]
        return rooms
