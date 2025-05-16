from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.models.models import User, UserType, Accommodation, Address, UserAccommodation, SubscriptionType
from app.routers import schemas
from app.routers.schemas import UserDetail, AccommodationDetail, AddressResponse, ExternalConnection


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
    user = (
        db.query(
            User.id.label("id"),
            User.username.label("username"),
            User.full_name.label("full_name"),
            User.email.label("email"),
            User.activation_date.label("activation_date"),
            User.blocked_date.label("blocked_date"),
            User.created_date.label("created_date"),
            UserType.name.label("type"),
            SubscriptionType.name.label("subscription_type"),
            Address.id.label("billing_id"),
            Address.name.label("billing_name"),
            Address.email.label("billing_email"),
            Address.tax_number.label("billing_tax"),
            Address.country.label("billing_country"),
            Address.postcode.label("billing_postcode"),
            Address.city.label("billing_city"),
            Address.street.label("billing_street"),
            Address.street_number.label("billing_street_number"),
            Address.floor.label("billing_floor"),
            Address.door.label("billing_door")
        )
        .join(User.user_type)
        .outerjoin(Address, Address.id == User.billing_address_id)
        .join(SubscriptionType, SubscriptionType.id == User.subscription_type_id)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserDetail(
        id=user.id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        status='blocked' if user.blocked_date else 'active' if user.activation_date else 'pending',
        type=user.type,
        activation_date=user.activation_date,
        blocked_date=user.blocked_date,
        created_date=user.created_date,
        subscription_type=user.subscription_type,
        billing_info=AddressResponse(
            id=user.billing_id,
            name=user.billing_name,
            email=user.billing_email,
            tax=user.billing_tax,
            country=user.billing_country,
            postcode=user.billing_postcode,
            city=user.billing_city,
            street=user.billing_street,
            street_number=user.billing_street_number,
            floor=user.billing_floor,
            door=user.billing_door
        )
    )


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
        .join(Accommodation.address)
        .filter(UserAccommodation.user_id == user_id)
        .all()
    )

    return [format_accommodation(row) for row in results]


def format_accommodation(row) -> dict:
    return {
        "id": row.id,
        "name": row.display_name,
        "active": row.active,
        "address": f'({row.country}) {row.postcode} {row.city}, {row.street} {row.street_number}'
    }


def get_accommodation_detail(user_id: int, accommodation_id: int, db: Session):
    result = (
        db.query(
            Accommodation.id.label("id"),
            Accommodation.display_name.label("name"),
            Accommodation.active.label("is_active"),
            Accommodation.created_date,
            Accommodation.szallas_hu_external_id.label("szallas_hu_id"),
            Accommodation.szallas_hu_external_ref.label("szallas_hu_ref"),
            Accommodation.vendegem_external_id.label("vendegem_id"),
            Accommodation.vendegem_external_ref.label("vendegem_ref"),
            Accommodation.contact_name,
            Accommodation.contact_phone,
            Accommodation.contact_email,
            Accommodation.reg_number,
            Address.id,
            Address.country,
            Address.postcode,
            Address.city,
            Address.street,
            Address.street_number,
            Address.floor,
            Address.door
        )
        .join(UserAccommodation, UserAccommodation.accommodation_id == Accommodation.id)
        .join(User, User.id == UserAccommodation.user_id)
        .join(Accommodation.address)
        .filter(
            UserAccommodation.user_id == user_id,
            Accommodation.id == accommodation_id
        )
        .first()
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    return AccommodationDetail(
        id=result.id,
        name=result.name,
        status='active' if result.is_active else 'inactive',
        szallas_hu=ExternalConnection(
            id=result.szallas_hu_id,
            ref=result.szallas_hu_ref
        ),
        vendegem=ExternalConnection(
            id=result.vendegem_id,
            ref=result.vendegem_ref
        ),
        contact_name=result.contact_name,
        contact_email=result.contact_email,
        contact_phone=result.contact_phone,
        created_date=result.created_date,
        reg_number=result.reg_number,
        address=AddressResponse(
            id=result.id,
            country=result.country,
            postcode=result.postcode,
            city=result.city,
            street=result.street,
            street_number=result.street_number,
            floor=result.floor,
            door=result.door
        )
    )
