import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from dotenv import load_dotenv

load_dotenv()



LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR,"app_logs.log")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

if LOG_LEVEL not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    LOG_LEVEL = "INFO"


LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s"
)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    force=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(LOG_FILE, maxBytes=2_000_000, backupCount=5),
    ],
)

logger = logging.getLogger('QAChatBoat')