import random
import string
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from starlette import status

from app.models.models import User, UserType, Accommodation, Address, UserAccommodation, SubscriptionType
from app.routers import schemas
from app.routers.schemas import UserDetail, AccommodationDetail, AddressModel, ExternalConnection, UserUpdateRequest, \
    UserPasswordUpdateRequest
from app.services import accommodation_service
from app.services.auth_service import USER_NAME


def login(username: str, password: str, db: Session):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.encrypted_secret):
        return None
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).options(joinedload(User.user_type)) \
        .filter((User.email == username) | (User.username == username)) \
        .first()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password
    # TODO: éles környezetben módosítani -> jelszavakat titkosítottan 1 irányba kódolhatóan tárolni
    # return pwd_context.verify(plain_password, hashed_password)


def create_user(user_request: schemas.UserCreate, logged_user, db: Session):
    db_user = db.query(User).filter(User.email == user_request.email).first()
    user_type = db.query(UserType).filter(UserType.name == 'Felhasználó').first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    new_user = User()
    # new_user.username = uuid.uuid4()
    new_user.full_name = user_request.name
    new_user.email = user_request.email

    new_user.type_id = user_type.id
    new_user.created_date = datetime.now()
    new_user.activation_date = datetime.now()
    new_user.created_by = logged_user[USER_NAME]
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return format_user_response_data(new_user, 0)


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
        number_of_acc = accommodation_service.number_of_accommodation_by_user_id(db, user.id)
        response.append(format_user_response_data(user, number_of_acc))

    return response


def format_user_response_data(user, number_of_acc) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "number_of_accommodations": number_of_acc,
        "status": 'blocked' if user.blocked_date else 'active' if user.activation_date else 'pending'
    }


def find_user_details_by_user_id(user_id: int, db: Session):
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
        .outerjoin(SubscriptionType, SubscriptionType.id == User.subscription_type_id)
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
        billing_info=AddressModel(
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
        .join(Accommodation.address, isouter=True)
        .filter(UserAccommodation.user_id == user_id)
        .all()
    )

    return [format_accommodation(row) for row in results]


def format_accommodation(row) -> dict:
    address_parts = [
        f'({row.country})' if row.country else None,
        row.postcode,
        row.city,
        row.street,
        row.street_number
    ]

    address_string = ', '.join([str(part).strip() for part in address_parts if part is not None and str(part).strip()])
    if not address_string:
        address_string = 'Nincs cím megadva'

    return {
        "id": row.id,
        "name": row.display_name,
        "active": row.active,
        "address": address_string
    }


def get_accommodation_detail(user_id: int, accommodation_id: int, db: Session):
    result = (
        db.query(
            Accommodation.id.label("accommodation_id"),
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
        .join(Accommodation.address, isouter=True)
        .filter(
            UserAccommodation.user_id == user_id,
            Accommodation.id == accommodation_id
        )
        .first()
    )

    if result is None:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    return AccommodationDetail(
        id=result.accommodation_id,
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
        address=AddressModel(
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


def find_user_by_id(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Felhasználó (ID: {user_id}) nem található."
        )
    return user


def activate_user(user_id: int, logged_user, db: Session):
    user = find_user_by_id(user_id, db)

    user.blocked_date = None
    user.activation_date = datetime.now()
    user.modified_by = logged_user[USER_NAME]
    user.modified_date = datetime.now()

    db.commit()


def inactivate_user(user_id: int, logged_user, db: Session):
    user = find_user_by_id(user_id, db)

    user.activation_date = None
    user.blocked_date = datetime.now()
    user.modified_by = logged_user[USER_NAME]
    user.modified_date = datetime.now()

    db.commit()


def update_user_and_billing_info(user_id: int, update_request: UserUpdateRequest, logged_user, db: Session):
    user = find_user_by_id(user_id, db)

    user.full_name = update_request.full_name
    user.email = update_request.email
    user.modified_by = logged_user[USER_NAME]
    user.modified_date = datetime.now()

    biu = update_request.billing_info
    if biu:
        uba = user.billing_address
        if not uba:
            uba = Address()
            uba.created_by = logged_user[USER_NAME]
            uba.created_date = datetime.now()
        else:
            uba.modified_by = logged_user[USER_NAME]
            uba.modified_date = datetime.now()

        uba.name = biu.name
        uba.email = biu.email
        uba.tax_number = biu.tax
        uba.postcode = biu.postcode
        uba.country = biu.country
        uba.city = biu.city
        uba.street = biu.street
        uba.street_number = biu.street_number
        uba.floor = biu.floor
        uba.door = biu.door

        db.add(uba)
        user.billing_address = uba

    db.add(user)
    db.commit()


def change_user_pass(user_id: int, update_pass_request: UserPasswordUpdateRequest, logged_user, db: Session):
    if update_pass_request.old_password == update_pass_request.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"The old and the new password can not be the same")

    user = find_user_by_id(user_id, db)
    if not verify_password(update_pass_request.old_password, user.encrypted_secret):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials")

    user.encrypted_secret = update_pass_request.new_password
    user.modified_by = logged_user[USER_NAME]
    user.modified_date = datetime.now()
    db.add(user)
    db.commit()


def admin_password_reset(user_id: int, logged_user, db: Session):
    user = find_user_by_id(user_id, db)

    user.encrypted_secret = generate_simple_password()
    user.modified_by = logged_user[USER_NAME]
    user.modified_date = datetime.now()
    db.add(user)
    # TODO: email küldés a felhasználónak a megadott email címére a kigenerált ideiglenes jelszóval
    db.commit()


def generate_simple_password():
    letters = string.ascii_letters
    digits = string.digits
    all_chars = letters + digits + string.punctuation

    length = random.randint(6, 12)
    password = [
        random.choice(letters),
        random.choice(digits)
    ]

    remaining_length = length - len(password)
    password.extend(random.choice(all_chars) for _ in range(remaining_length))

    random.shuffle(password)
    return "".join(password)
