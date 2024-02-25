from sqlalchemy import Column, Integer, String, Date, func, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class Contact(Base):
    """
    SQLAlchemy model representing a contact.

     Attributes:
         id (int): Primary key for the contact.
         name (str): Name of the contact.
         lastname (str): Last name of the contact.
         email (str): Email address of the contact.
         phone_number (str): Phone number of the contact.
         birthday (str): Birthday of the contact.
         user_id (int): Foreign key referencing the associated user.
         user (relationship): Relationship attribute representing the association with the User model.
    """

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(50), index=True)
    last_name = Column(String(50), index=True)
    email = Column(String(50), unique=True, index=True)
    phone_number = Column(String(50), index=True)
    birth_date = Column(Date())
    extra_data = Column(String(150), nullable=True)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="notes")

    def __repr__(self) -> str:
        return f"Contact({self.first_name} {self.last_name}, email: {self.email}, number: {self.phone_number}, birthdate: {self.birth_date}, extra data: {self.extra_data})"

class User(Base):
    """
    SQLAlchemy model representing a user.

    Attributes:
        id (int): Primary key for the user.
        username (str): Username of the user.
        email (str): Email address of the user (unique).
        password (str): Password of the user.
        created_at (DateTime): Timestamp indicating when the user was created.
        avatar (str): Filepath to the user's avatar (nullable).
        refresh_token (str): Refresh token for the user (nullable).
        confirmed (bool): Flag indicating whether the user is confirmed.
    """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)