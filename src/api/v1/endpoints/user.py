from fastapi import APIRouter, Depends, Body, HTTPException
from src.core.security import get_current_active_user
from src.db.repositories.user import UserRepository
from src.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.schemas import UserProfileCreate

router = APIRouter()



@router.post("/save-user")
async def create_or_update_user(
    request: UserProfileCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    repo = UserRepository(db)
    user = await repo.create_or_update_user(
        user_id=current_user["uid"],profile_data=request,email=current_user["email"])
    return user