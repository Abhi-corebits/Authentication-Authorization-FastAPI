from sqlalchemy import Column, Integer, String, Boolean
from database import Base

# Database Model (Our table structure)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    hashed_pwd = Column(String , nullable=False)
    is_active = Column(Boolean , default=True)