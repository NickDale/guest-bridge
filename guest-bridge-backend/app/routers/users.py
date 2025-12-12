from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.routers import schemas
from app.services import user_service
from app.services.auth_service import has_admin_role, verify_user_access, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

admin_router = APIRouter(
    prefix="/users",
    tags=["Users - Admin feature"],
    dependencies=[Depends(has_admin_role)],
)


@admin_router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
def create_user(user_creation_request: schemas.UserCreate, db: Session = Depends(get_db),
                logged_user=Depends(get_current_user)):
    return user_service.create_user(user_creation_request, logged_user, db)


@admin_router.get("/", response_model=None)
def list_users(expect: Optional[str] = Query(None),
               types: Optional[str] = Query(None),
               db: Session = Depends(get_db)):
    return user_service.list_users_by_filter(expect, types, db)


@admin_router.patch("/{user_id}/activate", response_model=None)
def activate_user_by_id(user_id: int, logged_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_service.activate_user(user_id, logged_user, db)


@admin_router.delete("/{user_id}/inactivate", response_model=None)
def inactivate_user_by_id(user_id: int, logged_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_service.inactivate_user(user_id, logged_user, db)


@router.get("/{user_id}", response_model=schemas.UserDetail)
def read_user_details_by_user_id(user_id: int, db: Session = Depends(get_db),
                                 verified_user=Depends(verify_user_access)):
    return user_service.find_user_details_by_user_id(user_id, db)


@router.patch("/{user_id}", response_model=None)
def update_user_id(user_id: int, update_request: schemas.UserUpdateRequest,
                   db: Session = Depends(get_db), verified_user=Depends(verify_user_access)):
    return user_service.update_user_and_billing_info(user_id, update_request, verified_user, db)


@router.get("/{user_id}/accommodations", response_model=None)
def list_user_accommodations(user_id: int, db: Session = Depends(get_db), verified_user=Depends(verify_user_access)):
    return user_service.get_accommodations_by_user_id(user_id, db)


@router.get("/{user_id}/accommodations/{accommodation_id}", response_model=schemas.AccommodationDetail)
def user_accommodation_details_by_accommodation_id(user_id: int, accommodation_id: int,
                                                   logged_user=Depends(verify_user_access),
                                                   db: Session = Depends(get_db)):
    return user_service.get_accommodation_detail(user_id, accommodation_id, db)


@router.patch("/{user_id}/change-password", response_model=None)
def user_password_change_by_user_id(user_id: int, update_pass_request: schemas.UserPasswordUpdateRequest,
                                    logged_user=Depends(verify_user_access),
                                    db: Session = Depends(get_db)):
    return user_service.change_user_pass(user_id, update_pass_request, logged_user, db)


@admin_router.patch("/{user_id}/reset-password", response_model=None)
def user_password_reset_by_user_id(user_id: int,
                                   logged_user=Depends(verify_user_access),
                                   db: Session = Depends(get_db)):
    return user_service.admin_password_reset(user_id, logged_user, db)
