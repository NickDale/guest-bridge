from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.models import User, UserType, Accommodation, Address, UserAccommodation
from app.routers import schemas
from app.routers.schemas import UserDetail


def login(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.encrypted_secret):
        return None
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).options(joinedload(User.user_type)).filter(User.username == username).first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password
    # TODO: change it
    # return pwd_context.verify(plain_password, hashed_password)


def create_user(user: schemas.UserCreate, db: Session):
    # todo: finish
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def list_users_by_filter(expect: str, types: str, db: Session):
    if types:
        typess = [t.strip().lower() for t in types.split(',')]
        users = db.query(User).join(User.user_type).filter(func.lower(UserType.name).in_(typess)).all()
    else:
        users = db.query(User).all()

    if expect:
        users = db.query(User).join(User.user_type).filter(
            func.lower(UserType.name).not_in([t.strip().lower() for t in expect.split(',')])
        ).all()

    response = []
    for user in users:
        response.append({
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "status": 'blocked' if user.blocked_date else 'active' if user.activation_date else 'pending'
        })

    return response


def find_user_by_id(user_id: int, db: Session):
    user = db.query(User).join(User.user_type).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'type': user.user_type.name,
        'activation_date': user.activation_date,
        'blocked_date': user.blocked_date
    }


def get_accommodations_by_user_id(user_id: int, db: Session):
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
            "active": active,
            "address": f'({country}) {postcode} {city}, {street} {street_number}'
        })

    return response


def get_accommodation_detail(user_id: int, accommodation_id: int, db: Session):
    result = (
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
        .filter(
            UserAccommodation.user_id == user_id,
            Accommodation.id == accommodation_id
        )
        .first()
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    id, display_name, active, country, postcode, city, street, street_number = result

    return {
        "id": id,
        "name": display_name,
        "active": active,
        "address": f'({country}) {postcode} {city}, {street} {street_number}'
    }
