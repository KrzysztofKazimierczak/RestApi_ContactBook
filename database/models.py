from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class Contact(Base):
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
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    refresh_token = Column(String(255), nullable=True)