from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.food_log import FoodLog
from src.models.schemas import FoodLogBatchCreate
from typing import List
from datetime import datetime, timezone,date
from sqlalchemy import func, select,extract
from typing import Dict
from calendar import monthrange

class FoodLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_food_log_batch(
    self,
    user_id: str,
    batch_data: FoodLogBatchCreate
    ) -> List[FoodLog]:
        logs = []
    
        for item in batch_data.items:
            # Calculate nutrition values
            calories = item.weight_grams * item.calories_per_gram
            protein = item.weight_grams * item.nutrients.protein_g / 100
            carbs = item.weight_grams * item.nutrients.carbohydrates_g / 100
            fats = item.weight_grams * item.nutrients.fats_g / 100

            log = FoodLog(
                user_id=user_id,
                food_name=item.name,
                weight_grams=item.weight_grams,
                calories_consumed=calories,
                protein_g=protein,
                carbs_g=carbs,
                fats_g=fats,
                meal_type=batch_data.meal_type,
                notes=batch_data.notes,
                image_url=batch_data.image_url
            )
            logs.append(log)
            self.db.add(log)

        await self.db.commit()
        return logs


    async def get_user_logs(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[FoodLog]:
        result = await self.db.execute(
            select(FoodLog)
            .where(FoodLog.user_id == user_id)
            .order_by(FoodLog.logged_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
    
    # In your FoodLogRepository class (src/db/repositories/food_log.py)


    async def get_todays_summary(self, user_id: str) -> dict:
        """Get today's nutritional summary for a user"""
        today = datetime.now(timezone.utc).date()
        
        result = await self.db.execute(
            select(
                func.sum(FoodLog.calories_consumed).label("total_calories"),
                func.sum(FoodLog.protein_g).label("total_protein"),
                func.sum(FoodLog.carbs_g).label("total_carbs"),
                func.sum(FoodLog.fats_g).label("total_fats")
            )
            .where(FoodLog.user_id == user_id)
            .where(func.date(FoodLog.logged_at) == today)
        )
        
        summary = result.first()
        
        return {
            "date": today.isoformat(),
            "total_calories": summary.total_calories or 0,
            "total_protein": summary.total_protein or 0,
            "total_carbs": summary.total_carbs or 0,
            "total_fats": summary.total_fats or 0
        }
    
    async def get_monthly_summary(
        self, 
        user_id: str, 
        year: int, 
        month: int
    ) -> Dict[date, dict]:
        """Get nutritional summary for each day of a specified month"""
        # First get the actual logged data
        result = await self.db.execute(
            select(
                func.date(FoodLog.logged_at).label("log_date"),
                func.sum(FoodLog.calories_consumed).label("total_calories"),
                func.sum(FoodLog.protein_g).label("total_protein"),
                func.sum(FoodLog.carbs_g).label("total_carbs"),
                func.sum(FoodLog.fats_g).label("total_fats")
            )
            .where(FoodLog.user_id == user_id)
            .where(extract('year', FoodLog.logged_at) == year)
            .where(extract('month', FoodLog.logged_at) == month)
            .group_by(func.date(FoodLog.logged_at))
        )
        # Convert query results to a dictionary
        logged_data = {
            row.log_date: {
                "total_calories": row.total_calories or 0,
                "total_protein": row.total_protein or 0,
                "total_carbs": row.total_carbs or 0,
                "total_fats": row.total_fats or 0
            }
            for row in result.all()
        }
        
        # Create a complete month dictionary with all dates
        _, num_days = monthrange(year, month)
        monthly_data = {}
        
        for day in range(1, num_days + 1):
            current_date = date(year, month, day)
            monthly_data[current_date] = logged_data.get(
                current_date,
                {
                    "total_calories": 0,
                    "total_protein": 0,
                    "total_carbs": 0,
                    "total_fats": 0
                }
            )
        
        return monthly_data
