from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.food_log import FoodLog
from src.models.schemas import FoodLogBatchCreate
from typing import List

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