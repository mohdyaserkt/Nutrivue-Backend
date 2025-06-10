from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from src.core.security import get_current_active_user
from src.db.repositories.food_log import FoodLogRepository
from src.db.session import get_db
from src.models.schemas import FoodLogResponse,FoodLogBatchCreate,DailyNutritionSummary,MonthlyNutritionResponse,DailyDetailsResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
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


@router.get("/log/today", response_model=DailyNutritionSummary)
async def get_todays_nutrition_summary(
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    repo = FoodLogRepository(db)
    return await repo.get_todays_summary(current_user["uid"])

# In your food_log.py router file

@router.get("/log/monthly/{year}/{month}", response_model=MonthlyNutritionResponse)
async def get_monthly_nutrition_summary(
    year: int,
    month: int,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    # Validate month input
    if month < 1 or month > 12:
        raise HTTPException(
            status_code=400,
            detail="Month must be between 1 and 12"
        )
    
    repo = FoodLogRepository(db)
    daily_summaries = await repo.get_monthly_summary(
        current_user["uid"],
        year,
        month
    )
    
    return {
        "year": year,
        "month": month,
        "daily_summaries": daily_summaries
    }

# In your food_log.py router file

@router.get("/log/daily/{target_date}", response_model=DailyDetailsResponse)
async def get_daily_details(
    target_date: date,
    current_user: dict = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    repo = FoodLogRepository(db)
    try:
        return await repo.get_daily_details(
            current_user["uid"],
            target_date
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )