from typing import Annotated

from fastapi import APIRouter, Depends

from app.services.auth_service import get_current_user, USER_NAME

router = APIRouter(prefix="/tests", tags=["API protection tests endpoints"])


@router.get("/public-data")
def login():
    return {"ok"}


@router.get("/protected-data")
def read_protected_data(user: Annotated[int, Depends(get_current_user)]):
    return {
        "message": "titkos adatok.",
        "user": user[USER_NAME]
    }
