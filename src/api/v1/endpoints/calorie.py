from fastapi import APIRouter, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from src.core.security import get_current_active_user
from src.services.gemini import analyze_food_image
from src.models.schemas import CalorieAnalysisResponse

router = APIRouter()

@router.post("/analyze", response_model=CalorieAnalysisResponse)
async def analyze_food(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_active_user),
    force_refresh: bool = False
):
    try:
        # Quick validation before processing
        if not file.content_type or not file.content_type.startswith("image/"):
            return JSONResponse(
                status_code=400,
                content={"message": "Only image files allowed"}
            )
        
        # Ensure file is readable
        await file.seek(0)
        return await analyze_food_image(file, force_refresh)
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Food analysis failed",
                "detail": str(e)
            }
        )
    finally:
        await file.close()