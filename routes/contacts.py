from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import ContactModel
from repository import contacts as repository_contacts
from database.models import User
from services.auth import auth_service

router = APIRouter(prefix='/contacts')

rate_limit = RateLimiter(times=10, seconds=60)


@router.post("/", response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(rate_limit)])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Create new contact

    Args:
        body (ContactModel): Data for the new contact.
        db (Session, optional): SQLAlchemy database session.
        current_user (User, optional):  The authenticated user.

    Returns:
        ContactModel: The created contact.
    """
    return await repository_contacts.create_contact(body, current_user, db)


@router.get("/", response_model=list[ContactModel], description='No more than 10 requests per minute',
            dependencies=[Depends(rate_limit)])
async def get_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    """
    Get all contacts

    Args:
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to retrieve.. Defaults to 20.
        db (Session, optional): SQLAlchemy database session.
        current_user (User, optional):The authenticated user

    Raises:
        HTTPException: negative number
        HTTPException: limit less than or equal to skip

    Returns:
        List[ContactModel]: The list of contacts.
    """
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A negative number is used.")
    elif limit <= skip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The limit is less than or equal to the skip.")

    contact = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contact


@router.get("/{contact_id}", response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(rate_limit)])
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    """
    Get contact by ID

    Args:
        contact_id (int): ID of the contact to retrieve.
        db (Session, optional): SQLAlchemy database session.
        current_user (User, optional): The authenticated user.

    Raises:
        HTTPException: Contact not found

    Returns:
        ContactModel: The requested contact.
    """

    contact = await repository_contacts.get_contact(contact_id, current_user, db)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.put("/{contact_id}", response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(rate_limit)])
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    """
    Update contact

    Args:
        contact_id (int): ID of the contact to update.
        body (ContactModel): Data for the updated contact.
        db (Session, optional): SQLAlchemy database session.
        current_user (User, optional): The authenticated user.

    Raises:
        HTTPException: Contact not found

    Returns:
        ContactModel: The updated contact.
    """

    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.delete("/{contact_id}", response_model=ContactModel, description='No more than 10 requests per minute',
            dependencies=[Depends(rate_limit)])
async def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Delete contact

    Args:
        contact_id (int): ID of the contact to delete.
        db (Session, optional): SQLAlchemy database session.
        current_user (User, optional): The authenticated user.

    Raises:
        HTTPException: Contact not found

    Returns:
        ContactModel: The deleted contact.
    """

    contact = await repository_contacts.delete_contact(contact_id, current_user, db) 

    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact

@router.get("/birthday/", response_model=List[ContactModel], description='No more than 10 requests per minute',
            dependencies=[Depends(rate_limit)])
async def get_upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    """
    Get upcoming birthdays

    Args:
        db (Session, optional): SQLAlchemy database session.
        current_user (User, optional): The authenticated user.

    Raises:
        HTTPException: Contact not found

    Returns:
        List[ContactModel]: The list of upcoming birthdays.
    """

    contact = await repository_contacts.get_upcoming_birthdays(current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact