from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.params import Query
from sqlalchemy import func, text
from sqlalchemy.orm import Session, joinedload

from app.models.models import User, UserType, Accommodation, UserAccommodation, Address
from app.routers import schemas
from app.services.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=List[schemas.UserRead])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# GET /users – összes felhasználó lekérése
@router.get("/", response_model=list[schemas.UserRead])
def read_users(expect: Optional[str] = Query(None),
               types: Optional[str] = Query(None),
               db: Session = Depends(get_db)):
    if types:
        typess = [t.strip().lower() for t in types.split(',')]
        users = db.query(User).join(User.user_type).filter(func.lower(UserType.name).in_(typess)).all()
    else:
        users = db.query(User).all()

    if expect:
        users = db.query(User).join(User.user_type).filter(
            func.lower(UserType.name).not_in([t.strip().lower() for t in expect.split(',')])
        ).all()
    return users


@router.get("/{user_id}", response_model=schemas.UserRead, response_model_by_alias=True)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/accommodations", response_model=None)
def read_user(user_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            Accommodation.id,
            Accommodation.display_name,
            Accommodation.active,
            Address.country,
            Address.postcode,
            Address.city,
            Address.street,
            Address.street_number
        )
        .join(UserAccommodation, UserAccommodation.accommodation_id == Accommodation.id)
        .join(User, User.id == UserAccommodation.user_id)
        .outerjoin(Address, Address.id == User.billing_address_id)
        .filter(UserAccommodation.user_id == user_id)
        .all()
    )

    response = []
    for id, display_name, active, country, postcode, city, street, street_number in results:
        response.append({
            "id": id,
            "name": display_name,
            "active":  active,
            "address": f'({country}) {postcode} {city}, {street} {street_number}'
        })

    return response


@router.get("/{user_id}/accommodations/{accommodation_id}", response_model=None)
def get_accommodation_details(user_id: int, db: Session = Depends(get_db)):
    results = (
        db.query(
            Accommodation.id,
            Accommodation.display_name,
            Accommodation.active,
            Address.country,
            Address.postcode,
            Address.city,
            Address.street,
            Address.street_number
        )
        .join(UserAccommodation, UserAccommodation.accommodation_id == Accommodation.id)
        .join(User, User.id == UserAccommodation.user_id)
        .outerjoin(Address, Address.id == User.billing_address_id)
        .filter(UserAccommodation.user_id == user_id)
        .all()
    )

    response = []
    for id, display_name, active, country, postcode, city, street, street_number in results:
        response.append({
            "id": id,
            "name": display_name,
            "active":  active,
            "address": f'({country}) {postcode} {city}, {street} {street_number}'
        })

    return response