from sqlalchemy.orm import Session

from app.services.vendegem.vendegem_connector import Vendegem


def list_all_accommodation_from_vendegem(db:Session):
    vendegem = Vendegem(user='vendegem.sync@gmail.com', password='C$3kkpoint00')
    return vendegem.visible_accommodations()