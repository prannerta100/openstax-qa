from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    OPENAI_CERTIFICATE: str = str(
        Path(__file__).parent.parent / "trustbundle.pem"
    )

settings = Settings()
