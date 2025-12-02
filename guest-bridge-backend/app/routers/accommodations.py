from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.routers.schemas import RoomMappingSchema, SynHistorySchema, AccommodationCreationRequest, \
    ExternalAuth2FAVerifyRequest, ExternalLoginRequest, SessionStatusCheck
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
def list_all_visible_vendegem_items():
    return connector_service.list_all_accommodation_from_vendegem()


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


@router.post("/{accommodation_id}/{connection_type}/login", response_model=None)
async def external_auth(accommodation_id: int,
                        connection_type: str,
                        ext_login_request: ExternalLoginRequest,
                        logged_user=Depends(get_current_user),
                        db: Session = Depends(get_db)):
    return connector_service.external_login(accommodation_id, connection_type, ext_login_request,logged_user, db)


@router.post("/{accommodation_id}/{connection_type}/session-status-check", response_model=None)
async def external_auth(accommodation_id: int,
                        connection_type: str,
                        status_check: SessionStatusCheck):
    return connector_service.session_status_check(accommodation_id, connection_type, status_check.session_id)


@router.post("/{accommodation_id}/{connection_type}/verify", response_model=None)
async def external_auth_2fa_verify(accommodation_id: int,
                                   connection_type: str,
                                   verify_request: ExternalAuth2FAVerifyRequest,
                                   logged_user=Depends(get_current_user)
                                   ):
    return connector_service.external_login_verification(
        accommodation_id, connection_type, verify_request, logged_user
    )
