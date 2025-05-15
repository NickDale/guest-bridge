base_url = "https://vendegem.hu/api"
accommodation_url = "/felhasznalo-szallashelyei"
auth_url = "/authenticate?remember-me=false"
reservations_url = "/foglalasEgyseg"
my_rooms_url = "/lakoegysegek"
new_reservation = "/foglalas/letrehozas"

vendegem_hun_id = "YWIyODE1NjItYjZlMy00Mzk3LWE1MDYtMjU1MzFmNzgxOTYx"
vendegem_guest_status = "ERKEZO"
vendegem_reservation_mode = "KOZVETITO_ONLINE"
vendegem_reservation_type = "SZABADIDOS_EGYENI"

default_headers = {
    'Accept': 'application/json, text/plain'
}

DATE_FORMAT = '%Y-%m-%d'


class Accommodation:
    def __init__(self, accommodation_id: None, szId=None):
        self.id = accommodation_id
        self.szId = szId
        self.rooms = []

    def find_room_id_by_szallas_hu_name(self, room_name: str):
        for room in self.rooms:
            if room['name'] == room_name \
                    or (room_name in room['name'] or room[
                'name'] in room_name):  # TODO: need a better mapping or SAME NAMES
                return room
        return None