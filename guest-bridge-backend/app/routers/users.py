from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi.params import Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers import schemas
from app.services import user_service
from app.services.auth_service import get_current_user, has_admin_role, verify_user_access

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

admin_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(has_admin_role)],
)


@admin_router.post("/", response_model=List[schemas.UserRead])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)


@admin_router.get("/", response_model=None)
def read_users(expect: Optional[str] = Query(None),
               types: Optional[str] = Query(None),
               db: Session = Depends(get_db)):
    return user_service.list_users_by_filter(expect, types, db)


@router.get("/{user_id}", response_model=schemas.UserDetail)
def read_user(user_id: int, db: Session = Depends(get_db), verified_user=Depends(verify_user_access)):
    return user_service.find_user_by_id(user_id, db)


@router.get("/{user_id}/accommodations", response_model=None)
def read_user(user_id: int, db: Session = Depends(get_db),
              verified_user=Depends(verify_user_access)):
    return user_service.get_accommodations_by_user_id(user_id, db)


@router.get("/{user_id}/accommodations/{accommodation_id}", response_model=schemas.AccommodationDetail)
def get_accommodation_details(user_id: int, accommodation_id: int,
                              logged_user=Depends(verify_user_access),
                              db: Session = Depends(get_db)):
    return user_service.get_accommodation_detail(user_id, accommodation_id, db)
