from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache
from typing import Dict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        extra='allow'

    )
    stability_api_key: str = Field(
...,
        description='API key for Stability AI')
    openai_api_key: str = Field(
        ..., description="API key for OpenAI",
    )
    file_paths: Dict[str, str]={
        "generation_instruction_file_path": "./generation_system_instructions.txt", 
"evaluation_system_instructions_file_path": "./evaluation_system_instructions.txt"
    }
    models: Dict[str, str]={
    "generation_model": "gpt-4o", 
    "evaluation_model": "gpt-4o"

}
    max_iterations: int=10


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.
    
    :return: An instance of Settings containing the configuration.
    """
    print("Loading settings from environment variables...")
    return Settings()

app_settings=get_settings()