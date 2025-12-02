BASE_URL = "https://vendegem.hu/api"
ACCOMMODATION_URL = "/felhasznalo-szallashelyei"
AUTH_URL = "/authenticate?remember-me=false"
RESERVATIONS_URL = "/foglalasEgyseg"
MY_ROOMS_URL = "/lakoegysegek"
NEW_RESERVATION = "/foglalas/letrehozas"

VENDEGEM_HUN_ID = "YWIyODE1NjItYjZlMy00Mzk3LWE1MDYtMjU1MzFmNzgxOTYx"
VENDEGEM_GUEST_STATUS = "ERKEZO"
VENDEGEM_RESERVATION_MODE = "KOZVETITO_ONLINE"
VENDEGEM_RESERVATION_TYPE = "SZABADIDOS_EGYENI"

DEFAULT_HEADERS = {
    'Accept': 'application/json, text/plain'
}

DATE_FORMAT = '%Y-%m-%d'
KEY_VENDEGEM_ROOM_ID = 'id'
KEY_SZALLAS_HU_ROOM_NAME = 'sz_hu_name'

VENDEGEM_RESERVATION_EXT_ID = 'foglalasEgysegkulsoId'

class VendegemAccommodation:
    def __init__(self, accommodation_id: None, name: str, owner: str, szId=None):
        self.id = accommodation_id
        self.szId = szId
        self.name = name
        self.owner = owner
        self.rooms = []

    def set_mapping(self, mapped_rooms: dict):
        for vendegem_id, sz_hu_name in mapped_rooms.items():
            for room in self.rooms:
                if room[KEY_VENDEGEM_ROOM_ID] == vendegem_id:
                    room[KEY_SZALLAS_HU_ROOM_NAME] = sz_hu_name

    def find_room_id_by_szallas_hu_name(self, room_name: str):
        for room in self.rooms:
            if room[KEY_SZALLAS_HU_ROOM_NAME] == room_name:  # or (room_name in room['name'] or room['name'] in room_name):
                return room[KEY_VENDEGEM_ROOM_ID]
        return None
