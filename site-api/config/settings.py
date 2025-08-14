from starlette.config import Config
import json
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
dotenv_file = os.path.join(BASE_DIR, '.env')

config = Config(dotenv_file)

def parse_json_credentials(value):
    if value is None:
        return None
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format for credentials: {value[:50]}...")

class Settings:
    ALLOWED_ORIGINS = config("ALLOWED_ORIGINS", cast=str, default="*")
    GCLOUD_PROJECT_ID = config("GCLOUD_PROJECT_ID", cast=str)
    GCLOUD_REGION = config("GCLOUD_REGION", cast=str, default="europe-west2")
    LOG_LEVEL = config("LOG_LEVEL", cast=str, default="INFO")
    GOOGLE_APPLICATION_CREDENTIALS = config("GOOGLE_APPLICATION_CREDENTIALS", cast=parse_json_credentials, default=None)

settings = Settings()