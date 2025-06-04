from pydantic import BaseModel
from typing import Optional,List

class TokenData(BaseModel):
    uid: str
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    pass

class UserInDB(UserBase):
    uid: str
    disabled: bool = False

class ProtectedResponse(BaseModel):
    message: str
    user_info: dict

class NutrientInfo(BaseModel):
    protein_g: float
    carbohydrates_g: float
    fats_g: float

class FoodItem(BaseModel):
    name: str
    calories_per_gram: float
    nutrients: NutrientInfo


class CalorieAnalysisResponse(BaseModel):
    items: List[FoodItem]
    healthy_alternatives: str  # Optional


class Nutrients(BaseModel):
    protein_g: float
    carbohydrates_g: float
    fats_g: float

class FoodItem(BaseModel):
    name: str
    calories: float
    nutrients: Nutrients
    serving_size: Optional[str] = None
