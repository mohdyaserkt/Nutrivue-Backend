from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List, Optional, Union

class Settings(BaseSettings):
    PROJECT_NAME: str = "nutrivue"
    PROJECT_DESCRIPTION: str = "Industry-grade Calorie Monitor"
    VERSION: str = "1.0.0"
    
    API_V1_STR: str = "/api/v1"
    ENV: Optional[str] = "dev"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip("[]").replace('"', '').replace("'", "")
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        raise ValueError(v)

    @property
    def RELOAD(self):
        return self.ENV == "dev"

    @property
    def WORKERS(self):
        return 1 if self.RELOAD else 4

    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = "./serviceAccountKey.json"
    
    # Database
    DATABASE_URL_SYNC: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    
    # APIs
    GOOGLE_API_KEY: str
    
    # Redis
    REDIS_URL: str
    CACHE_EXPIRE_HOURS: int

    class Config:
        case_sensitive = True
        env_file = ".env"

def get_settings():
    return Settings()
