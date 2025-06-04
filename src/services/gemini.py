import google.generativeai as genai
from datetime import timedelta
from src.models.schemas import CalorieAnalysisResponse
from src.core.cache import image_cache_key_builder
from fastapi import UploadFile, HTTPException
from fastapi_cache import FastAPICache
from src.config.config import get_settings



PROMPT_TEMPLATE = """
Analyze this food image and return JSON with:
- food items (name, calories per gram, nutrients)
- healthy alternatives

"""

async def analyze_food_image(
    file: UploadFile,
    force_refresh: bool = False
) -> CalorieAnalysisResponse:
    """Analyze food image with proper cache handling"""
    try:
        # Generate cache key manually since decorator has issues
        cache_key = image_cache_key_builder(
            func=analyze_food_image,
            namespace="gemini-analysis",
            file=file
        )
        
        # Check cache if not forcing refresh
        if not force_refresh:
            cached_result = await FastAPICache.get_backend().get(key=cache_key)
            if cached_result:
                return CalorieAnalysisResponse.parse_raw(cached_result)
        
        # Process with Gemini if no cache hit
        GeminiApiKey=get_settings().GOOGLE_API_KEY
        print(GeminiApiKey)
        genai.configure(api_key=GeminiApiKey)
        model = genai.GenerativeModel("gemini-1.5-flash")
        await file.seek(0)
        image_bytes = await file.read()
        
        response = model.generate_content(
            contents=[
                PROMPT_TEMPLATE,
                {"mime_type": file.content_type, "data": image_bytes}
            ],
            generation_config={
                "response_mime_type": "application/json",
                "response_schema":CalorieAnalysisResponse ,
                "temperature": 0.3
            }
        )
        
        # Validate and parse response
        result = CalorieAnalysisResponse.parse_raw(response.text)
        
        # Cache the result
        await FastAPICache.get_backend().set(cache_key, result.json(), expire=timedelta(hours=24))

        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
    finally:
        await file.seek(0)