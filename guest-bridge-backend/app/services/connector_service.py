from sqlalchemy.orm import Session

from app.models.models import Accommodation, UserAccommodation, User
from app.services.vendegem.vendegem_connector import Vendegem


def list_all_accommodation_from_vendegem(db: Session):
    vendegem = connect_to_vendegem()
    return vendegem.visible_accommodations()


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
    return Vendegem(user='', password='')
