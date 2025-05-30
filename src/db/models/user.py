from sqlalchemy import Column, String, Boolean
from src.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # Firebase UID
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)