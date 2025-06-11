from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User
from src.models.schemas import UserProfileCreate
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update_user(self, user_id: str,email:str,profile_data: UserProfileCreate)-> User:
        user = await self.db.get(User, user_id)
        
        if not user:
            user = User(id=user_id,email=email,**profile_data.model_dump(exclude={"customCalorie"}),
                target_calories=self._calculate_calories(profile_data))
            self.db.add(user)
        else:
            for field, value in profile_data.model_dump().items():
                setattr(user, field, value)
            user.target_calories = self._calculate_calories(profile_data)

        await self.db.commit()
        return user
    

    def _calculate_calories(self, profile: UserProfileCreate) -> int:
        # Basic Harris-Benedict calculation
        if profile.gender == "male":
            bmr = 88.362 + (13.397 * profile.weight_kg) + (4.799 * profile.height_cm) - (5.677 * profile.age)
        else:
            bmr = 447.593 + (9.247 * profile.weight_kg) + (3.098 * profile.height_cm) - (4.330 * profile.age)
        
        activity_factors = {
            "sedentary": 1.2,
            "light": 1.375,
            "moderate": 1.55,
            "active": 1.725,
            "extra": 1.9
        }
        
        maintenance = bmr * activity_factors[profile.activity_level]
        
        if profile.goal == "lose":
            return int(maintenance * 0.85)
        elif profile.goal == "gain":
            return int(maintenance * 1.15)
        elif profile.goal=="custom":
            return int(profile.customCalorie)
        return int(maintenance)
    