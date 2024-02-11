from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database.models import Contact, User
from schemas import ContactModel, ContactUpdate
from datetime import date, timedelta

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birth_date=body.birth_date,
        extra_data=body.extra_data,
        user_id=user.id
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    db.close()
    return contact

async def get_contacts(skip: int, limit: int, user: User, db: Session) -> List[Contact]:
    contacts = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    db.close()
    return contacts

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    db.close()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, user: User, db: Session) -> Contact:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.birth_date = body.birth_date
        contact.extra_data = body.extra_data

        db.commit()
    return contact


async def delete_contact(contact_id: int, user: User, db: Session) -> Contact:
    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_upcoming_birthdays(user: User, db: Session):
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    contacts = db.query(Contact).filter(and_(Contact.birth_date >= today, Contact.birth_date <= seven_days_later, Contact.user_id == user.id)).all()
    db.close()
    return contacts

