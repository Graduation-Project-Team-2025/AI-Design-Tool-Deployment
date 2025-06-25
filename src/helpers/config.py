from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int


    HUGGING_FACE_TOKEN: str
    GITHUB_TOKEN: str
    DOCKERHUB_TOKEN: str
    
    FILE_ALLOWED_TYPES: List[str]
    FILE_ALLOWED_SIZE: int
    
    MODELS_WEIGHTS_PATH: str
    UPLOAD_FILES_PATH: str

    CONTROLNET_MODEL: str
    BASE_MODEL: str
    TRANSLATION_MODEL:str



    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
