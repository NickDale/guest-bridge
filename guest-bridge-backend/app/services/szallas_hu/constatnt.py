from enum import Enum

BASE_SZALLAS_HU_URL = 'https://admin.szallas.hu'
LOGIN_URL = BASE_SZALLAS_HU_URL + '/login/submit'
RESERVATION_DETAIL_URL = '/reservation/details?id='

DEFAULT_DAY_DELAY = 20
ALREADY_ARRIVED = 'Aktív: Megérkezett'


class Keys(Enum):
    NAME = 'Név'
    EMAIL = 'E-mail cím'
    GUST_NO = 'Utazók'
    ID = 'Azonosító'

    def __str__(self):
        return self.value
