from typing import List
from sqlalchemy.orm import Session
from database.models import Contact
from schemas import ContactModel, ContactUpdate
from datetime import date, timedelta

async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        phone_number=body.phone_number,
        birth_date=body.birth_date,
        extra_data=body.extra_data
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    db.close()
    return contact

    return db.query(Note).offset(skip).limit(limit).all()


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    db.close()
    return contacts

async def get_contact(contact_id: int, db: Session) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    db.close()
    return contact

async def update_contact(contact_id: int, body: ContactUpdate, db: Session) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name=body.first_name,
        contact.last_name=body.last_name,
        contact.email=body.email,
        contact.phone_number=body.phone_number,
        contact.birth_date=body.birth_date,
        contact.extra_data=body.extra_data
        db.commit()
    return contact

async def delete_contact(contact_id: int, db: Session) -> Contact:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_upcoming_birthdays(db: Session):
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    contacts = db.query(Contact).filter(
        (Contact.birth_date >= today) & (Contact.birth_date <= seven_days_later)
    ).all()
    db.close()
    return contacts

