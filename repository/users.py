from sqlalchemy.orm import Session
from database.models import User
from schemas import UserModel

async def get_user_by_email(email: str, db: Session) -> User:
    """
    Get user by email

    Args:
        email (str): Email of the user 
        db (Session): SQLAlchemy database session

    Returns:
        Type[User]: User object or None
    """

    return db.query(User).filter(User.email == email).first()

async def create_user(body: UserModel, db: Session) -> User:
    """
    Create new user

    Args:
        body (UserModel): Data for the new user
        db (Session): SQLAlchemy database session

    Returns:
        User: The created user
    """

    new_user = User(**body.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    Update refresh token

    Args:
        user (User): User object
        token (str | None): Refresh token
        db (Session): SQLAlchemy database session
    """

    user.refresh_token = token
    db.commit()

async def confirm_email(email: str, db: Session) -> None:
    """
    Confirm email

    Args:
        email (str): Email of the user
        db (Session): SQLAlchemy database session
    """

    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()

async def update_avatar(email, url: str, db: Session) -> User:
    """
    Update avatar

    Args:
        email (str): Email of the user
        url (str): URL of the avatar
        db (Session): SQLAlchemy database session

    Returns:
        User: The updated user
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user