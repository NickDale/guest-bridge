from sqlalchemy.orm import Session

from app.models.models import Accommodation, UserAccommodation, User
from app.services import accommodation_service
from app.services.vendegem.vendegem_connector import Vendegem

def list_all_accommodation_from_vendegem(db: Session):
    vendegem = connect_to_vendegem()
    return vendegem.visible_accommodations()


def check_accommodation_connection(accommodation_id: int, connection_type: str, db: Session):
    if 'SZALLAS_HU' == connection_type:
        return False

    if 'VENDEGEM' == connection_type:
        return True
        # accommodation = accommodation_service.find_accommodation_by_id(db, accommodation_id)
        # if accommodation is None:
        #     return False
        # else:
        #     vendegem = connect_to_vendegem()
        #     visible_accommodations_in_vendegem = vendegem.visible_accommodations
        #     try:
        #         found_accommodation = next(
        #             (ac for ac in visible_accommodations_in_vendegem if
        #              ac.name == accommodation['name'] and ac.id == accommodation['vendegem_external_id']),
        #             None
        #         )
        #         if found_accommodation:
        #             return True
        #     except Exception as e:
        #         print(f"Hiba történt a keresés során: {e}")
        #         return False

    return False


def list_rooms_for_accommodation(accommodation_id: int, db: Session):
    # TODO: validate user visibility for accomodation

    accommodation = (
        db.query(
            Accommodation.vendegem_external_id.label("vendegem_id"),
            Accommodation.vendegem_external_ref.label("vendegem_ref")
        )
        # .join(UserAccommodation, UserAccommodation.accommodation_id == Accommodation.id)
        # .join(User, User.id == UserAccommodation.user_id)
        .filter(
            # UserAccommodation.user_id == user_id,
            Accommodation.id == accommodation_id
        )
        .first()
    )
    print(accommodation.vendegem_id)
    vendegem = connect_to_vendegem()
    return vendegem.rooms_by_id(accommodation.vendegem_id)


def connect_to_vendegem() -> Vendegem:
    return Vendegem(user='vendegem.sync@gmail.com', password='C$3kkpoint0x0')
