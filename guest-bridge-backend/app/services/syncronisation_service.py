from datetime import datetime, timedelta

from colorama import Fore, Style
from playwright.sync_api import Page
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import SyncHistory, SyncHistoryDetail, Accommodation
from app.services import accommodation_service
from app.services.szallas_hu.constatnt import DEFAULT_DAY_DELAY
from app.services.szallas_hu.reservation import Reservation
from app.services.szallas_hu.szallas_hu_connection import collect_reservations
from app.services.vendegem.helper import VendegemAccommodation, VENDEGEM_RESERVATION_EXT_ID
from app.services.vendegem.vendegem_connection import connect_to_vendegem
from app.services.vendegem.vendegem_connector import Vendegem


def start_sync(page: Page, internal_accommodation_id: int, started_by_user_id: str,
               from_date: datetime = None, to_date: datetime = None):
    try:
        if from_date is None:
            from_date = datetime.now()
        if to_date is None:
            to_date = from_date + timedelta(days=DEFAULT_DAY_DELAY)

        db_session = next(get_db())
        accommodation = accommodation_service.accommodation_by_id(internal_accommodation_id, db_session)

        sync_history = sync_db_record_init(internal_accommodation_id, started_by_user_id, db_session)

        try:
            mappings = szallas_hu_vendem_mapping(db_session, accommodation_id=internal_accommodation_id)
            vendegem = connect_to_vendegem()

            selected_vendegem_accommodation = vendegem.find_accommodation_by_id(accommodation.vendegem_external_id)
            v_stored_reservations = vendegem.list_reservations(selected_vendegem_accommodation.id, from_date, to_date)
            selected_vendegem_accommodation.set_mapping(mappings)

            szallas_hu_reservations = collect_reservations(page, accommodation.szallas_hu_external_id, from_date,
                                                           to_date)
            cancelled_reservations, active_reservations = group_reservations(szallas_hu_reservations)

            for deleted_item in cancelled_reservations:
                for stored in v_stored_reservations:
                    if str(deleted_item.reservation_id) in stored['foglaloNev'].strip():
                        delete_from_vendegem(
                            vendegem,
                            sync_history.id,
                            str(deleted_item.reservation_id),
                            stored[VENDEGEM_RESERVATION_EXT_ID],
                            db_session
                        )
                    else:
                        print(
                            f"{Fore.YELLOW} Reservation [id = {str(deleted_item.reservation_id)}] "
                            f"deleted in szállás.hu but not exist in Vendégem {Style.RESET_ALL}")

            for active_item in active_reservations:
                reservation_found = False

                for stored in v_stored_reservations:
                    if active_item.guest_name.strip() == stored['foglaloNev'].strip():
                        reservation_found = True
                        if active_item.check_in == stored['mettol'] and active_item.check_out == stored['meddig']:
                            print("Már rögzítettük:", active_item)
                            continue
                        else:
                            delete_from_vendegem(
                                vendegem,
                                sync_history.id,
                                str(active_item.reservation_id),
                                stored[VENDEGEM_RESERVATION_EXT_ID],
                                db_session
                            )
                            reservation_found = False
                            print("Töröltök mert eltért --> újra felvesszük", active_item)

                if not reservation_found:
                    data = active_item.create_reservation_request_payload_to_vendegem(selected_vendegem_accommodation)
                    data_sync_to_vendegem(vendegem,
                                          sync_history.id,
                                          str(active_item.reservation_id),
                                          data,
                                          db_session
                                          )

            sync_history.status = 'OK'

        except Exception as e:
            sync_history.status = 'FAILED'
            sync_history.error_message = e
            print(e)

        db_session.add(sync_history)
        db_session.commit()

    except Exception as e:
        print(e)
        raise e
    finally:
        print("session close")
        pass


def delete_from_vendegem(vendegem: Vendegem,
                         sync_history_id: int,
                         reservation_id: str,
                         vendegem_room_id: str,
                         db: Session):
    sync_detail = init_delete_sync_detail_db_record(
        sync_history_id,
        reservation_id,
        vendegem_room_id
    )
    try:
        vendegem.delete_reservation_by_id(vendegem_room_id)
        sync_detail.status = 'OK'
    except Exception as e:
        print(e)
        sync_detail.status = 'FAILED'

    db.add(sync_detail)
    db.commit()


def sync_db_record_init(accommodation_id: int, started_by_user_id: str, db_session: Session):
    sync_history = SyncHistory()
    sync_history.accommodation_id = accommodation_id
    sync_history.created_date = datetime.now()
    sync_history.created_by = f'user_id:{started_by_user_id}'
    sync_history.status = 'STARTED'

    db_session.add(sync_history)
    db_session.commit()
    db_session.refresh(sync_history)

    return sync_history


def init_delete_sync_detail_db_record(sync_history_id: int, reservation_id: str, vendegem_room_id: str):
    sync_detail = SyncHistoryDetail()
    sync_detail.sync_id = sync_history_id
    sync_detail.type = 'DELETE'
    sync_detail.reservation_id = reservation_id
    sync_detail.created_date = datetime.now()
    # sync_detail.created_by(f'user_id:{started_by_user_id}')
    sync_detail.debug_message = \
        f"Szallas_hu foglalas [{reservation_id}] törlése a Vendegemből - szobaId[{vendegem_room_id}]"

    return sync_detail


def data_sync_to_vendegem(vendegem: Vendegem,
                          sync_history_id: int,
                          reservation_id: str,
                          vendegem_payload: dict,
                          db: Session):
    sync_detail = init_insert_sync_detail_db_record(sync_history_id, reservation_id)
    try:
        vendegem.create_reservation(request_payload=vendegem_payload)

        sync_detail.status = 'OK'
    except Exception as e:
        print(e)
        sync_detail.status = 'FAILED'

    db.add(sync_detail)
    db.commit()


def init_insert_sync_detail_db_record(sync_history_id: int, reservation_id: str):
    sync_detail = SyncHistoryDetail()
    sync_detail.sync_id = sync_history_id
    sync_detail.type = 'INSERT'
    sync_detail.reservation_id = reservation_id
    sync_detail.created_date = datetime.now()
    # sync_detail.created_by(f'user_id:{started_by_user_id}')
    sync_detail.debug_message = f"Szallas_hu foglalás [{reservation_id}] rögzítése a Vendegembe"

    return sync_detail


def szallas_hu_vendem_mapping(db: Session, accommodation_id: int) -> dict:
    room_mapping = accommodation_service.find_mapping_config_by_accommodation_id(
        db, accommodation_id=accommodation_id
    )
    return {
        mapping.vendegem_ext_room_id: mapping.szallas_hu_ext_room_name
        for mapping in room_mapping if mapping.szallas_hu_ext_room_name and mapping.vendegem_ext_room_id
    }


def find_correct_accommodation_in_vendegem(vendegem: Vendegem, accommodation: Accommodation) -> VendegemAccommodation:
    visible_accommodations_in_vendegem = vendegem.visible_accommodations
    try:
        found_accommodation = next(
            (ac for ac in visible_accommodations_in_vendegem if
             # ac.name == accommodation.display_name and
             ac.id == accommodation.vendegem_external_id),
            None
        )
        if found_accommodation:
            return found_accommodation
    except Exception as e:
        print(f"Hiba történt a keresés során: {e}")
        return None


def group_reservations(reservations: list[Reservation], cancelled_status_name: str = 'GUEST_CANCELED'):
    cancelled_reservations = [
        res for res in reservations
        if res.status.strip().upper() == cancelled_status_name.upper()
    ]

    active_reservations = [
        res for res in reservations
        if res.status.strip().upper() != cancelled_status_name.upper()
    ]

    return cancelled_reservations, active_reservations
