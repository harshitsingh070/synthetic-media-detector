from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "Synthetic Media Detection ML Service"
    version: str = "1.0.0"
    debug: bool = False
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    model_cache_dir: str = "./models"
    temp_dir: str = "./temp"
    
    # Model configurations
    image_model_name: str = "prithivMLmods/deepfake-detector-model-v1"
    audio_model_path: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
