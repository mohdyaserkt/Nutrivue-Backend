from fastapi import APIRouter, Depends
from src.core.security import get_current_active_user

router = APIRouter()

@router.get("/")
async def protected_root(current_user=Depends(get_current_active_user)):
    return {
        "message": f"Hello, {current_user.get('email')}! This is a protected route.",
        "user_info": current_user
    }

@router.post("/submit-data")
async def submit_data(
    data: dict,
    current_user=Depends(get_current_active_user)
):
    return {
        "message": "Data received successfully!",
        "user_uid": current_user.get("uid"),
        "submitted_data": data
    }