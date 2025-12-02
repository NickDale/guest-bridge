from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from app.models.models import Accommodation, RoomMapping, SyncHistory, Address, UserAccommodation
from app.routers.schemas import AccommodationCreationRequest
from app.services.auth_service import USER_NAME


def find_mapping_config_by_accommodation_id(db: Session, accommodation_id: int):
    results = db.query(RoomMapping).filter(RoomMapping.accommodation_id == accommodation_id).all()

    return results


def find_accommodation_by_id(db: Session, accommodation_id: int) -> dict | None:
    result = (
        db.query(
            Accommodation.id,
            Accommodation.display_name,
            Accommodation.active,
            Accommodation.vendegem_external_id,
            Accommodation.vendegem_external_ref
        )
        .filter(Accommodation.id == accommodation_id)
        .first()
    )
    if result:
        return find_accommodation_by_id_response_format(result)
    else:
        return None


def find_accommodation_by_id_response_format(row) -> dict:
    return {
        "id": row.id,
        "name": row.display_name,
        "active": row.active,
        "vendegem_external_id": row.vendegem_external_id,
        "vendegem_external_ref": row.vendegem_external_ref
    }


def accommodation_sync_histories(db: Session, accommodation_id: int):
    results = db.query(SyncHistory) \
        .outerjoin(SyncHistory.details) \
        .filter(SyncHistory.accommodation_id == accommodation_id) \
        .all()

    return results


def number_of_accommodation_by_user_id(db: Session, user_id: int) -> int:
    return db.query(func.count(UserAccommodation.id)).filter(UserAccommodation.user_id == user_id).scalar()


def create_new_accommodation(request: AccommodationCreationRequest, logged_user, db: Session):
    accommodation = db.query(Accommodation) \
        .filter(
        (Accommodation.reg_number == request.ntak_no)
        | (Accommodation.display_name == request.name)
        | (Accommodation.szallas_hu_external_id == request.szallas_hu_id)
    ).first()
    if accommodation:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Accommodation already registered with this NTAK number - {request.ntak_no} or name {request.name}'
        )

    new_accommodation = Accommodation()
    new_accommodation.display_name = request.name
    new_accommodation.active = True
    new_accommodation.szallas_hu_external_id = request.szallas_hu_id
    new_accommodation.vendegem_external_id = request.vendegem_id
    new_accommodation.vendegem_external_ref = request.vendegem_ref
    new_accommodation.contact_name = request.contact_name
    new_accommodation.contact_email = request.contact_email
    new_accommodation.contact_phone = request.contact_phone
    new_accommodation.reg_number = request.ntak_no

    address_request = request.address
    if address_request:
        new_address = Address()
        new_address.country = 'Magyarország'
        new_address.city = address_request.city
        new_address.postcode = address_request.postcode
        new_address.street = address_request.street
        new_address.street_number = address_request.street_number
        new_address.floor = address_request.floor
        new_address.door = address_request.door

        new_address.created_date = datetime.now()
        new_address.created_by = logged_user[USER_NAME]

        new_accommodation.address = new_address

    new_accommodation.created_date = datetime.now()
    new_accommodation.created_by = logged_user[USER_NAME]

    try:
        # db.add(new_accommodation)

        ua = UserAccommodation()
        ua.user_id = request.user_id
        ua.accommodation = new_accommodation
        ua.created_date = datetime.now()
        ua.created_by = logged_user[USER_NAME]

        db.add(ua)
        db.commit()
        db.refresh(new_accommodation)
        return {
            "id": new_accommodation.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {e}"
        )


def accommodation_by_id(accommodation_id: int, db: Session):
    accommodation = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    if not accommodation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Accommodation not exists with id - {accommodation_id}'
        )
    return accommodation

