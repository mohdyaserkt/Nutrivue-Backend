from pydantic import BaseModel
from typing import Optional

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