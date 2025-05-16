from datetime import datetime
from typing import Optional

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
    status: str
    email: str

    class Config:
        orm_mode = True


class AddressResponse(BaseModel):
    id: int
    name: Optional[str] = None
    email: Optional[str] = None
    tax: Optional[str] = None
    country: Optional[str]
    postcode: Optional[str]
    city: Optional[str]
    street: Optional[str]
    street_number: Optional[str]
    floor: Optional[str]
    door: Optional[str]


class UserDetail(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    type: str
    status: str
    activation_date: Optional[datetime]
    blocked_date: Optional[datetime]
    created_date: datetime
    subscription_type: str
    billing_info: AddressResponse


class AccommodationResponse:
    id: int
    display_name: str
    status: str
    address: str


class ExternalConnection(BaseModel):
    id: Optional[str]
    ref: Optional[str]


class AccommodationDetail(BaseModel):
    id: int
    name: str
    status: str
    address: AddressResponse
    szallas_hu: ExternalConnection
    vendegem: ExternalConnection
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    reg_number: Optional[str]
    created_date: datetime
