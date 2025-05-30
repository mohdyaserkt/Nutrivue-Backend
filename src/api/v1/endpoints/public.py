from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def public_root():
    return {"message": "Public endpoint - no authentication required"}

@router.get("/health")
async def health_check():
    return {"status": "healthy"}