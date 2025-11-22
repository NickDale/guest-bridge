from datetime import timedelta, datetime

from fastapi import HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from app.services import user_service
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = '123456789'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 10
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

TOKEN_USER_ID = "id"
TOKEN_USER_NAME = "sub"
TOKEN_EXP_DATE = "exp"
TOKEN_ROLE = "r"

USER_ID = 'user_id'
USER_NAME = 'user_name'
USER_ROLE = 'role'

AUTH_FAILED_MSG = 'Invalid credentials'
FORBIDDEN_MSG = 'Access denied'


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=AUTH_FAILED_MSG,
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get(TOKEN_USER_ID)
        if user_id is None:
            raise credentials_exception

        return {
            USER_ID: user_id,
            USER_NAME: payload.get(TOKEN_USER_NAME),
            USER_ROLE: payload.get(TOKEN_ROLE)
        }
    except JWTError:
        raise credentials_exception


async def has_admin_role(token: str = Depends(oauth2_scheme)):
    result = await get_current_user(token)

    if "ADMIN" != result[USER_ROLE].upper():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=FORBIDDEN_MSG
        )
    return True


def verify_user_access(user_id: int, current_user=Depends(get_current_user)):
    if "ADMIN" == current_user[USER_ROLE].upper():
        return current_user

    if user_id != current_user[USER_ID]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=FORBIDDEN_MSG)
    return current_user



def login(username: str, password: str, db: Session):
    user = user_service.login(username, password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return {
        "access_token": create_access_token(data={
            TOKEN_USER_NAME: user.username,
            TOKEN_USER_ID: user.id,
            TOKEN_ROLE: user.user_type.name.upper()
        }),
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.user_type.name.upper()
        }
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({TOKEN_EXP_DATE: expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
