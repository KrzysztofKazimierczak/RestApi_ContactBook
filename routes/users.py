import os
from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from database.db import get_db
from database.models import User
from repository import users as repository_users
from services.auth import auth_service
from schemas import UserDb

from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/users", tags=["users"])

rate_limit = RateLimiter(times=10, seconds=60)

@router.get("/me/", response_model=UserDb, dependencies=[Depends(rate_limit)])
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(),
                             current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'contact_book/{current_user.email}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'contact_book/{current_user.email}') \
        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user