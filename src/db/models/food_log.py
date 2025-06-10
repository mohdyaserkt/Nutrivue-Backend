from sqlalchemy import Column, String, Float, TIMESTAMP, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.db.base import Base

class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    user_id = Column(String, nullable=False)
    food_name = Column(String, nullable=False)
    weight_grams = Column(Float, nullable=False)
    calories_consumed = Column(Float, nullable=False)
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fats_g = Column(Float, nullable=False)
    logged_at = Column(TIMESTAMP, server_default=func.now())
    image_url = Column(String)
    meal_type = Column(String)
    notes = Column(Text)