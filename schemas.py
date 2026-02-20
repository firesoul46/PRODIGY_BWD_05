from pydantic import BaseModel, EmailStr, Field
from datetime import date
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr
    # Restrict password length to 72 characters
    password: str = Field(..., max_length=72)

class RoomCreate(BaseModel):
    title: str
    city: str
    price: float

class RoomResponse(RoomCreate):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    room_id: int
    check_in: date
    check_out: date

class ReviewCreate(BaseModel):
    room_id: int
    rating: int # We should check if this is between 1-5
    comment: str