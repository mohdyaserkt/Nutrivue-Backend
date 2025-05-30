from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_or_update_user(self, user_id: str, email: str, name: str = None):
        user = await self.db.get(User, user_id)
        
        if not user:
            user = User(id=user_id, email=email, name=name)
            self.db.add(user)
        else:
            user.email = email
            user.name = name if name else user.name
        
        await self.db.commit()
        return user