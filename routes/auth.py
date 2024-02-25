from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from database.db import get_db
from schemas import UserModel, UserResponse, TokenModel
from repository import users as repository_users
from services.auth import auth_service
from services.email import send_email

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    """
    New user registration

    Args:
        body (UserModel): Data for the new user.
        background_tasks (BackgroundTasks): Background tasks to execute.
        request (Request): The incoming request.
        db (Session, optional): SQLAlchemy database session.

    Raises:
        HTTPException: Account already exists

    Returns:
        dict: Response containing the new user and a confirmation message.
    """

    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Account already exists")
    
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    background_tasks.add_task(send_email, new_user.email, new_user.username, request.base_url)

    return {"user": new_user, "detail": "User successfully created. Check your email for confirmation."}


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    User login


    Args:
        body (OAuth2PasswordRequestForm, optional): Form containing user credentials.
        db (Session, optional): SQLAlchemy database session.

    Raises:
        HTTPException: Invalid email
        HTTPException: Email not confirmed
        HTTPException: Invalid password

    Returns: 
        dict: Response containing access and refresh tokens
    """

    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email")
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not confirmed")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})

    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}



@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    Refresh access token

    Args:
        credentials (HTTPAuthorizationCredentials, optional): Credentials containing the refresh token.(security).
        db (Session, optional): SQLAlchemy database session.

    Raises:
        HTTPException: Invalid refresh token.

    Returns:
        dict: Response containing a new access token and refresh token.
    """

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)

    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})

    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: Session = Depends(get_db)):
    """
    Confirm email

    Args:
        token (str): confirmation token.
        db (Session, optional): SQLAlchemy database session.

    Raises:
        HTTPException: Verification error.

    Returns:
        dict: Response message.
    """

    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    
    await repository_users.confirm_email(email, db)
    return {"message": "Email confirmed"}
