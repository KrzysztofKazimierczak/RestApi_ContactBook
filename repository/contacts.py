from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database.models import Contact, User
from schemas import ContactModel
from datetime import date, timedelta

async def create_contact(body: ContactModel, user: User, db: Session) -> Contact:
    """
    Create new contact

    Args:
        body (ContactModel): Data for the new contact.
        user (User): The authenticated user.
        db (Session): SQLAlchemy database session.

    Returns:
        Contact: The created contact.
    """


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
    """
    Get all contacts

    Args:
        skip (int): Number of records to skip
        limit (int): Maximum number of records to retrieve
        user (User): The authenticated user
        db (Session): SQLAlchemy database session

    Returns:
        List[Contact]: The list of contacts
    """

    contacts = db.query(Contact).filter(Contact.user_id == user.id).offset(skip).limit(limit).all()
    db.close()
    return contacts

async def get_contact(contact_id: int, user: User, db: Session) -> Contact:
    """
    Get contact by ID

    Args:
        contact_id (int): ID of the contact to retrieve
        user (User): The authenticated user
        db (Session): SQLAlchemy database session

    Returns:
        Contact: The requested contact
    """

    contact = db.query(Contact).filter(and_(Contact.id == contact_id,Contact.user_id == user.id)).first()
    db.close()
    return contact

async def update_contact(contact_id: int, body: ContactModel, user: User, db: Session) -> Contact:
    """
    Update contact

    Args:
        contact_id (int): ID of the contact to update
        body (ContactModel): Data for the updated contact
        user (User): The authenticated user
        db (Session): SQLAlchemy database session

    Returns:
        Contact: The updated contact
    """

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
    """
    Delete contact

    Args:
        contact_id (int): ID of the contact to delete
        user (User): The authenticated user
        db (Session): SQLAlchemy database session

    Returns:
        Contact: The deleted contact
    """

    contact = db.query(Contact).filter(and_(Contact.id == contact_id, Contact.user_id == user.id)).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

async def get_upcoming_birthdays(user: User, db: Session):
    """
    Get upcoming birthdays

    Args:
        user (User): The authenticated user
        db (Session): SQLAlchemy database session

    Returns:
        List[Contact]: The list of upcoming birthdays
    """
    today = date.today()
    seven_days_later = today + timedelta(days=7)
    contacts = db.query(Contact).filter(and_(Contact.birth_date >= today, Contact.birth_date <= seven_days_later, Contact.user_id == user.id)).all()
    db.close()
    return contacts

