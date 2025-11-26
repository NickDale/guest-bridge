from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.routers.schemas import RoomMappingSchema, SynHistorySchema, AccommodationCreationRequest
from app.services import connector_service, accommodation_service
from app.services.auth_service import get_current_user, has_admin_role

router = APIRouter(
    prefix="/accommodations",
    tags=["Accommodation"],
    dependencies=[Depends(get_current_user)],
)

admin_router = APIRouter(
    prefix="/accommodations",
    tags=["Accommodation"],
    dependencies=[Depends(has_admin_role)],
)


@router.get("/vendegem/visible-accommodations", response_model=None)
def list_all_visible_vendegem_items(db: Session = Depends(get_db)):
    return connector_service.list_all_accommodation_from_vendegem(db)


@router.get("/vendegem/{accommodation_id}/rooms", response_model=None)
def list_all_visible_vendegem_items(accommodation_id: int, db: Session = Depends(get_db)):
    return connector_service.list_rooms_for_accommodation(accommodation_id, db)


@admin_router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_new_accommodation(acc_request: AccommodationCreationRequest,
                             db: Session = Depends(get_db),
                             logged_user=Depends(get_current_user)
                             ):
    return accommodation_service.create_new_accommodation(acc_request, logged_user, db)


@router.get("/{accommodation_id}/{connection_type}/connection-check", response_model=bool)
def accommodation_connection_check(accommodation_id: int, connection_type: str, db: Session = Depends(get_db)):
    return connector_service.check_accommodation_connection(accommodation_id, connection_type, db)


@router.get("/{accommodation_id}/mapping-configuration", response_model=list[RoomMappingSchema])
def accommodation_mapping(accommodation_id: int, db: Session = Depends(get_db)):
    return accommodation_service.find_mapping_config_by_accommodation_id(db, accommodation_id)


# todo: validation --> user láthatja e ezt az accomodationt
@router.get("/{accommodation_id}/sync-history", response_model=list[SynHistorySchema])
def accommodation_sync_histories(accommodation_id: int, db: Session = Depends(get_db)):
    return accommodation_service.accommodation_sync_histories(db, accommodation_id)
