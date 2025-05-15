from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.routers import schemas
from app.routers.schemas import LoginResponse
from app.services import user_service

router = APIRouter(prefix="/authentications", tags=["auth"])


@router.post("/login", response_model=schemas.LoginResponse)
def login(request: schemas.Login, db: Session = Depends(get_db)):
    user = user_service.login(request.username, request.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return LoginResponse(
        id=user.id,
        username=user.username,
        full_name=user.full_name,
        email=user.email,
        role=user.user_type.name,
    )
