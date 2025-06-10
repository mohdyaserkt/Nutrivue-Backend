from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.core.security import get_current_active_user
from src.db.repositories.food_log import FoodLogRepository
from src.db.session import get_db
from src.models.schemas import FoodLogResponse,FoodLogBatchCreate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter()

@router.post("/log/batch", response_model=List[FoodLogResponse])
async def log_food_batch(
    batch_data: FoodLogBatchCreate,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    repo = FoodLogRepository(db)
    try:
        logs = await repo.create_food_log_batch(
            current_user["uid"],
            batch_data
        )
        return logs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/logs", response_model=List[FoodLogResponse])
async def get_food_logs(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    repo = FoodLogRepository(db)
    return await repo.get_user_logs(current_user["uid"])