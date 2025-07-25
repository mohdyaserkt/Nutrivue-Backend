from fastapi import APIRouter
from fastapi import Depends
from src.api.v1.endpoints import  public, protected,user,calorie,food_log
from src.core.security import get_current_active_user
api_router = APIRouter()

api_router.include_router(public.router, tags=["public"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    protected.router,
    prefix="/protected",
    tags=["protected"],
)

api_router.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)]  # Protect all user routes
)


api_router.include_router(
    calorie.router,
    prefix="/calorie",
    tags=["calorie"],
    dependencies=[Depends(get_current_active_user)]  # Protected route
)


api_router.include_router(
    food_log.router,
    prefix="/food",
    tags=["food logs"],
    dependencies=[Depends(get_current_active_user)]
)