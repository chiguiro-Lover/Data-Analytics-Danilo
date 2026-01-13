import os
from dotenv import load_dotenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH)

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
REGION = os.getenv("REGION", "americas")

if RIOT_API_KEY is None:
    raise ValueError("RIOT_API_KEY not found in environment variables")
