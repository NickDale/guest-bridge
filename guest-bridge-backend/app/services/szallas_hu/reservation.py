from datetime import datetime

from app.services.vendegem.helper import VendegemAccommodation, VENDEGEM_HUN_ID, VENDEGEM_RESERVATION_MODE, \
    VENDEGEM_RESERVATION_TYPE, VENDEGEM_GUEST_STATUS, DATE_FORMAT


class Reservation:

    def __init__(self, reservation_data: dict):
        self.reservation_id = reservation_data['reservationId']
        self.guest_name = reservation_data['guestFullName'] + ' [' + str(reservation_data['reservationId']) + ']'
        self.guest_count = reservation_data['guestCount']
        self._set_phone_number(reservation_data['guestPhone'])
        self.status = reservation_data['status']

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

    def create_reservation_request_payload_to_vendegem(self, accommodation: VendegemAccommodation):
        data = {
            'szallashelyKulsoId': accommodation.id,
            'megrendeloNev': self.guest_name,
            'megrendeloEmailCim': self.guest_email,
            'megrendeloTelefonSzam': self.guest_phone,
            'megrendeloAllampolgarsag': {
                'kulsoId': VENDEGEM_HUN_ID
            },
            'vendegekSzama': int(self.guest_count),
            'foglalasMod': VENDEGEM_RESERVATION_MODE,
            'piaciSzegmens': VENDEGEM_RESERVATION_TYPE,
            'foglalasEgysegek': []
        }

        for sz_hu_room_name, price in self.rooms.items():
            room_price = self.__calculate_room_price()
            data['foglalasEgysegek'].append(
                {
                    'allapot': VENDEGEM_GUEST_STATUS,
                    'erkezesDatum': self.check_in,
                    'utazasDatum': self.check_out,
                    'lakoegysegDto': {
                        'szallashelyKulsoId': accommodation.id,
                        'kulsoId': accommodation.find_room_id_by_szallas_hu_name(sz_hu_room_name)
                    },
                    'ejszakaAra': room_price
                }
            )

        return data

    def __calculate_room_price(self) -> float:
        start_date = datetime.strptime(self.check_in, DATE_FORMAT)
        end_date = datetime.strptime(self.check_out, DATE_FORMAT)

        return (float(self.full_price) / (end_date - start_date).days) / int(self.room_count)

