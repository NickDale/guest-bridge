from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.routers import schemas
from app.services import auth_service

router = APIRouter(prefix="/authentications", tags=["Authentication"])


# @router.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     auth_resp = auth_service.login(username=form_data.username, password=form_data.password, db=db)
#     return {"access_token": auth_resp['access_token'], "token_type": auth_resp['token_type']}


@router.post("/login")
def login(request: schemas.Login, db: Session = Depends(get_db)):
    return auth_service.login(username=request.username, password=request.password, db=db)
