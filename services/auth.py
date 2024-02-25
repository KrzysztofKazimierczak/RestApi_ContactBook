import os
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from database.db import get_db
from repository import users as repository_users
from dotenv import load_dotenv
load_dotenv()

class Auth:
    """
    Authentication class.

    Attributes:
        pwd_context (CryptContext): Password hashing context.
        SECRET_KEY (str): Secret key for token encoding and decoding.
        ALGORITHM (str): Algorithm used for token encoding and decoding.
        oauth2_scheme (OAuth2PasswordBearer): OAuth2 password bearer for token retrieval.
    """
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

    def verify_password(self, plain_password, hashed_password):
        """
        Verify the plain password against the hashed password.

        Args:
            plain_password (str): The plain text password.
            hashed_password (str): The hashed password.

        Returns:
            bool: True if passwords match, False otherwise.
        """

        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    async def create_access_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create an access token.

        Args:
            data (dict): The data to encode in the token._
            expires_delta (Optional[float], optional): The expiration time of the token. Defaults to None.

        Returns:
            str: The encoded access token.
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "access_token"})
        encoded_access_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_access_token

    async def create_refresh_token(self, data: dict, expires_delta: Optional[float] = None):
        """
        Create a refresh token.

        Args:
            data (dict): The data to encode in the token.
            expires_delta (Optional[float], optional): The expiration time of the token. Defaults to None.

        Returns:
            str: The encoded refresh token.
        """

        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + timedelta(seconds=expires_delta)
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire, "scope": "refresh_token"})
        encoded_refresh_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token: str):
        """
        Decode a refresh token.

        Args:
            refresh_token (str): The refresh token.

        Raises:
            HTTPException: Invalid scope for token
            HTTPException: Could not validate credentials

        Returns:
            str: The decoded refresh token.
        """

        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
        Get the current user.

        Args:
            token (str, optional): The access token.
            db (Session, optional): The database session.

        Raises:
            credentials_exception: Could not validate credentials

        Returns:
            Dict: The current user.
        """

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload["sub"]
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data: dict):
        """
        Create an email token.

        Args:
            data (dict): The data to encode in the token.

        Returns:
            str: The encoded email token.
        """

        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({"iat": datetime.utcnow(), "exp": expire})
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token
    
    async def get_email_from_token(self, token: str):
        """
        Get the email from the token.

        Args:
            data Dict: The data to encode in the token.

        Raises:
            HTTPException: Invalid token for email verification

        Returns:
            str: The email from the token.
        """

        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            email = payload["sub"]
            return email
        except JWTError as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                                detail="Invalid token for email verification")


auth_service = Auth()