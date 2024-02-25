from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr



class ContactModel(BaseModel):
    """
    Schema for the response of a contact.
    """
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    extra_data: str = None

    class Config:
        from_attributes = True


class UserModel(BaseModel):
    """
    Schema for the user registration.
    """
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    """
    Schema for user data retrieved from the database.
    """
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """
    Schema for the response after user creation.
    """
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    """
    Schema for the request containing an email address.
    """
    access_token: str
    refresh_token: str
    token_type: str = "bearer"