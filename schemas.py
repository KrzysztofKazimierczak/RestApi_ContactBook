from datetime import date
from pydantic import BaseModel



class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    birth_date: date
    extra_data: str = None

class ContactUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    email: str = None
    phone_number: str = None
    birth_date: date = None
    extra_data: str = None
