from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base


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

    def __repr__(self) -> str:
        return f"Contact({self.first_name} {self.last_name}, email: {self.email}, number: {self.phone_number}, birthdate: {self.birth_date}, extra data: {self.extra_data})"