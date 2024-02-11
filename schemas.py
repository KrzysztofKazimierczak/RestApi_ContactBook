from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr



class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    extra_data: str = None

    class Config:
        from_attributes = True

class ContactUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone_number: str = None
    birth_date: date = None
    extra_data: str = None


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"