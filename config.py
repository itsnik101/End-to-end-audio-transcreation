import os
import sys
import logging
from pathlib import Path
from dotenv import load_dotenv

# Base System Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
RAW_SCRIPTS_DIR = DATA_DIR / "raw_scripts"
AUDIO_CACHE_DIR = DATA_DIR / "audio_cache"

# Idempotently generate necessary filesystem folders
RAW_SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Central log file location tracking path
LOG_FILE_PATH = LOGS_DIR / "audix_system.log"

# Unified Platform Logging Engine Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(LOG_FILE_PATH), encoding="utf-8")
    ]
)

logger = logging.getLogger("audix.config")

# Force explicit absolute path resolution for the .env file
ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.exists():
    load_dotenv(dotenv_path=ENV_PATH)
    logger.info(f"Successfully loaded environmental definitions from: {ENV_PATH}")
else:
    logger.error(f"Environmental definitions missing on disk. Checked path: {ENV_PATH}")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
if not GEMINI_API_KEY:
    raise RuntimeError(f"Critical System Initialization Failure: 'GEMINI_API_KEY' variable could not be parsed. Checked path: {ENV_PATH}")

API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN", "").strip()
if not API_BEARER_TOKEN:
    raise RuntimeError("Security Safeguard Failure: 'API_BEARER_TOKEN' environment variable must be set.")

API_BACKEND_URL = os.getenv("API_BACKEND_URL", "http://127.0.0.1:8000").strip().rstrip('/')

DEFAULT_MODEL = "gemini-2.5-flash"
TRANSCREATION_TEMPERATURE = 0.3
DB_PATH = DATA_DIR / "pipeline_history.db"