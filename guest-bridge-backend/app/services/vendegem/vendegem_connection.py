from app.core.config import settings
from app.services.vendegem.vendegem_connector import Vendegem


def connect_to_vendegem() -> Vendegem:
    return Vendegem(user=settings.VENDEGEM_USER, password=settings.VENDEGEM_SECRET)
