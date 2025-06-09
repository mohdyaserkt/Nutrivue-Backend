from pydantic import BaseModel
from typing import Optional,List
from enum import Enum
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




class Gender(str, Enum):
    male = "male"
    female = "female"

class ActivityLevel(str, Enum):
    sedentary = "sedentary"
    light = "light"
    moderate = "moderate"
    active = "active"
    extra = "extra"

class Goal(str, Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"
    custom="custom"

class UserProfileCreate(BaseModel):
    name:str
    age: int
    gender: Gender
    weight_kg: float
    height_cm: float
    activity_level: ActivityLevel
    goal: Goal
    

class UserProfileResponse(UserProfileCreate):
    id: str
    target_calories: Optional[int]
    created_at: str