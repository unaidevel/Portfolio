from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from fastapi import APIRouter
from pydantic import EmailStr, PastDate, BaseModel
import uuid
from typing import List
from enum import Enum


router = APIRouter()


class User(SQLModel):
    id: uuid.UUID = Field(default=uuid.uuid4, primary_key=True)
    username: str = Field(max_length=15)
    full_name: str = Field(max_length=20)
    email: EmailStr = Field(unique=True)
    birth_date: date

    booking: List['Booking'] = Relationship(back_populates='user')


class UserInDb(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


class CourtChoices(str, Enum):
    tennis = 'Tennis court'
    padel = 'Padel court'

class Court(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    court_type: CourtChoices

    booking: List['Booking'] = Relationship(back_populates='court')


class Booking(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    booking_date: date
    user_id: uuid.UUID = Field(foreign_key='User.id')
    court_id: uuid.UUID = Field(foreign_key='Court.id')


    user: User = Relationship(back_populates='booking')
    court: Court = Relationship(back_populates='booking')


