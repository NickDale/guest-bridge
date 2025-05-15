from sqlalchemy.orm import Session, joinedload

from app.models.models import User


def authenticate_user(username: str, password: str, db: Session):
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
