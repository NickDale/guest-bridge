from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


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


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    id: int
    username: Optional[str] = None
    full_name: str
    status: Optional[str] = None
    email: str

    class Config:
        orm_mode = True


class AddressModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    tax: Optional[str] = None
    country: Optional[str] = None
    postcode: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    floor: Optional[str] = None
    door: Optional[str] = None


class UserDetail(BaseModel):
    id: int
    username: Optional[str] = None
    email: str
    full_name: Optional[str] = None
    type: str
    status: str
    activation_date: Optional[datetime]
    blocked_date: Optional[datetime]
    created_date: datetime
    subscription_type: Optional[str] = None
    billing_info: AddressModel


class AccommodationResponse:
    id: int
    display_name: str
    status: str
    address: str


class AccommodationCreationRequest(BaseModel):
    name: str
    ntak_no: str
    user_id: int
    szallas_hu_id: str
    vendegem_id: Optional[str] = None
    vendegem_ref: Optional[str] = None
    contact_name: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None
    address: Optional[AddressModel] = None


class ExternalConnection(BaseModel):
    id: Optional[str]
    ref: Optional[str]


class AccommodationDetail(BaseModel):
    id: int
    name: str
    status: str
    address: AddressModel
    szallas_hu: ExternalConnection
    vendegem: ExternalConnection
    contact_name: Optional[str]
    contact_phone: Optional[str]
    contact_email: Optional[str]
    reg_number: Optional[str]
    created_date: datetime


class RoomMappingSchema(BaseModel):
    id: int
    accommodation_id: int
    szallas_hu_ext_room_id: Optional[str] = None
    szallas_hu_ext_room_name: Optional[str] = None
    vendegem_ext_room_id: Optional[str]
    vendegem_ext_room_name: Optional[str]
    created_date: datetime
    created_by: Optional[str] = None

    class Config:
        from_attributes = True


class SynHistoryDetailSchema(BaseModel):
    id: int
    reservation_id: str
    debug_message: Optional[str] = None
    type: str
    status: str
    error_message: Optional[str] = None
    created_date: datetime
    created_by: Optional[str] = None


class SynHistorySchema(BaseModel):
    id: int
    accommodation_id: int
    debug_message: Optional[str] = None
    status: str
    error_message: Optional[str] = None
    details: list[SynHistoryDetailSchema]
    created_date: datetime
    created_by: Optional[str] = None


class BillingAddressUpdate(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    tax: Optional[str] = None
    postcode: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    floor: Optional[str] = None
    door: Optional[str] = None


class UserUpdateRequest(BaseModel):
    full_name: str
    email: str
    billing_info: Optional[BillingAddressUpdate] = None


class UserPasswordUpdateRequest(BaseModel):
    old_password: str
    new_password: str


class ExternalLoginRequest(BaseModel):
    username: str
    password: str


class ExternalAuth2FAVerifyRequest(BaseModel):
    session_id: str
    code: str


class SessionStatusCheck(BaseModel):
    session_id: str
