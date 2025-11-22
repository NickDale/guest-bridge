from enum import Enum

base_szallas_hu_url = 'https://admin.szallas.hu'
login_url = base_szallas_hu_url + '/login/submit'
reservation_detail_url = '/reservation/details?id='

DEFAULT_DAY_DELAY = 20
ALREADY_ARRIVED = 'Aktív: Megérkezett'


class Keys(Enum):
    NAME = 'Név'
    EMAIL = 'E-mail cím'
    GUST_NO = 'Utazók'
    ID = 'Azonosító'

    def __str__(self):
        return self.value