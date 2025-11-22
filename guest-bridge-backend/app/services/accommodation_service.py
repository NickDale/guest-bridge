from sqlalchemy.orm import Session

from app.models.models import Accommodation, RoomMapping, SyncHistory


def find_mapping_config_by_accommodation_id(db: Session, accommodation_id: int):
    results = db.query(RoomMapping).filter(RoomMapping.accommodation_id == accommodation_id).all()

    return results


def find_accommodation_by_id(db: Session, accommodation_id: int) -> dict | None:
    result = (
        db.query(
            Accommodation.id,
            Accommodation.display_name,
            Accommodation.active,
            Accommodation.vendegem_external_id,
            Accommodation.vendegem_external_ref
        )
        .filter(Accommodation.id == accommodation_id)
        .first()
    )
    if result:
        return find_accommodation_by_id_response_format(result)
    else:
        return None


def find_accommodation_by_id_response_format(row) -> dict:
    return {
        "id": row.id,
        "name": row.display_name,
        "active": row.active,
        "vendegem_external_id": row.vendegem_external_id,
        "vendegem_external_ref": row.vendegem_external_ref
    }


def accommodation_sync_histories(db: Session, accommodation_id: int):
    results = db.query(SyncHistory) \
        .join(SyncHistory.details) \
        .filter(SyncHistory.accommodation_id == accommodation_id) \
        .all()

    return results
