from pydantic import BaseModel, EmailStr


# API-n keresztül érkező bemenethez
class UserBase(BaseModel):
    name: str
    email: EmailStr  # automatikus email validáció


class Login(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    id: int
    username: str
    full_name: str
    email: str
    role: str

    class Config:
        orm_mode = True


# POST /users esetén (csak name és email kell)
class UserCreate(UserBase):
    pass  # ugyanaz, mint UserBase


# Válaszként visszaküldött struktúra
class UserRead(BaseModel):
    id: int
    username: str
    full_name: str
    email: str

    class Config:
        orm_mode = True


class AccommodationResponse:
    id: int
    display_name: str
    status: str
    address: str