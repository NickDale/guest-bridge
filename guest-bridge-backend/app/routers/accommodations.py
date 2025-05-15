from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services import connector_service

router = APIRouter(prefix="/connectors", tags=["connectors"])


@router.get("/vendegem/visible-accommodations", response_model=None)
def list_all_visible_vendegem_items(db: Session = Depends(get_db)):
    return connector_service.list_all_accommodation_from_vendegem(db)
