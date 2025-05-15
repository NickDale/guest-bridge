
from datetime import datetime
from colorama import Fore, Style

from app.services.szallas_hu.szallas_hu_connector import SzallasHu
from app.services.vendegem.vendegem_connector import Vendegem


class SyncProcess:
    def __init__(self):
        self.szallas_hu_app = SzallasHu(user='', password='')
        self.vendegem_app = Vendegem(user='', password='')

    def start_sync(self, to_date, from_date=datetime.now()):
        stored_reservations = self.vendegem_app.reservations(from_date, to_date)

        deleted_reservation_ids = self.szallas_hu_app.deleted_reservations(from_date, to_date)

        for dr_id in deleted_reservation_ids:
            for stored in stored_reservations:
                if str(dr_id) in stored['foglaloNev'].strip():
                    self.vendegem_app.delete_reservation_by_id(
                        stored['foglalasEgysegkulsoId']
                    )
                else:
                    print(
                        f"{Fore.YELLOW} Reservation [id = {str(dr_id)}] deleted in szállás.hu but not exist in Vendégem {Style.RESET_ALL}")

        reservations = self.szallas_hu_app.active_reservations(from_date, to_date)
        for r in reservations:
            reservation_found = False

            for stored in stored_reservations:
                if r.guest_name.strip() == stored['foglaloNev'].strip():
                    reservation_found = True
                    if r.check_in == stored['mettol'] and r.check_out == stored['meddig']:
                        print("Már rögzítettük:", r)
                        continue
                    else:
                        self.vendegem_app.delete_reservation_by_id(
                            stored['foglalasEgysegkulsoId']
                        )
                        reservation_found = False
                        print("Töröltök mert eltért --> újra felvesszük", r)

            if not reservation_found:
                self.vendegem_app.create_reservation(payload=r)