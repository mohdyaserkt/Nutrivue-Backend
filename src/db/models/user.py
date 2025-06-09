from sqlalchemy import Column, String, Boolean,Integer,Enum,Float,TIMESTAMP
from src.db.base import Base
from sqlalchemy.sql import func
class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)  # Firebase UID
    email = Column(String, unique=True, index=True)
    name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    age = Column(Integer, nullable=False)
    gender = Column(Enum('male', 'female', name='gender_types'), nullable=False)
    weight_kg = Column(Float, nullable=False)
    height_cm = Column(Float, nullable=False)
    activity_level = Column(
        Enum('sedentary', 'light', 'moderate', 'active', 'extra', name='activity_levels'),
        nullable=False
    )
    goal = Column(Enum('lose', 'maintain', 'gain','custom', name='goal_types'), nullable=False)
    target_calories = Column(Integer)
    created_at = Column(TIMESTAMP, server_default=func.now())