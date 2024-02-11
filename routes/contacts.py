from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import ContactModel, ContactUpdate
from repository import contacts as repository_contacts
from database.models import User
from services.auth import auth_service

router = APIRouter(prefix='/contacts')



@router.post("/", response_model=ContactModel)
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    return await repository_contacts.create_contact(body, current_user, db)


@router.get("/", response_model=list[ContactModel])
async def get_contacts(skip: int = 0, limit: int = 20, db: Session = Depends(get_db),
                        current_user: User = Depends(auth_service.get_current_user)):
    if skip < 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="A negative number is used.")
    elif limit <= skip:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The limit is less than or equal to the skip.")

    contact = await repository_contacts.get_contacts(skip, limit, current_user, db)
    return contact


@router.get("/{contact_id}", response_model=ContactModel)
async def get_contact(contact_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact(contact_id, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.put("/{contact_id}", response_model=ContactModel)
async def update_contact(contact_id: int, body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(contact_id, body, current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact


@router.delete("/{contact_id}", response_model=ContactModel)
async def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.delete_contact(contact_id, current_user, db)    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return contact

@router.get("/birthday/", response_model=List[ContactModel])
async def get_upcoming_birthdays(db: Session = Depends(get_db), current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_upcoming_birthdays(current_user, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found.")
    return contact