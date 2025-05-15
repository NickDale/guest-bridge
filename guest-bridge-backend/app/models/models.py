from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True, nullable=False)
    full_name = Column(String(200), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    billing_address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)
    type_id = Column(Integer, ForeignKey("user_types.id"), nullable=False)
    activation_date = Column(DateTime, nullable=True)
    blocked_date = Column(DateTime, nullable=True)
    subscription_type_id = Column(Integer, ForeignKey("subscription_types.id"), nullable=False)
    encrypted_secret = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=True)
    modified_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_type = relationship("UserType", back_populates="users")


class Accommodation(Base):
    __tablename__ = "accommodations"
    id = Column(Integer, primary_key=True, index=True)
    display_name = Column(String(200))
    active = Column(Boolean, default=True)
    szallas_hu_external_id = Column(String(255))
    szallas_hu_external_ref = Column(String(255))
    vendegem_external_id = Column(String(255))
    vendegem_external_ref = Column(String(255))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100), nullable=True)
    modified_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_date = Column(DateTime, nullable=True)
    deleted_by = Column(String(100), nullable=True)



class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(100))
    tax_number = Column(String(50))
    country = Column(String(20))
    postcode = Column(String(20))
    city = Column(String(50))
    street = Column(String(255))
    street_number = Column(String(10))
    floor = Column(String(10))
    door = Column(String(10))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100))
    modified_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class RoomMapping(Base):
    __tablename__ = "room_mappings"
    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"), nullable=False)
    szallas_hu_ext_room_id = Column(String(255))
    szallas_hu_ext_room_name = Column(String(50))
    vendegem_ext_room_id = Column(String(255))
    vendegem_ext_room_name = Column(String(50))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100))
    modified_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class SubscriptionType(Base):
    __tablename__ = "subscription_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)


class UserAccommodation(Base):
    __tablename__ = "user_accommodations"
    id = Column(Integer, primary_key=True, index=True)
    accommodation_id = Column(Integer, ForeignKey("accommodations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    created_by = Column(String(100), nullable=False)
    modified_by = Column(String(100))
    modified_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    deleted_date = Column(DateTime, nullable=True)
    deleted_by = Column(String(100), nullable=True)

    user = relationship("User", backref="user_accommodations")
    accommodation = relationship("Accommodation", backref="user_accommodations")


class UserType(Base):
    __tablename__ = "user_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="user_type")
