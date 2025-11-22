import logging
from datetime import datetime
from pathlib import Path
from .config import config

LOG_DIR = config.log_dir
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / f"search_mcp_{datetime.now().strftime('%Y%m%d')}.log"

logger = logging.getLogger("search_mcp")
logger.setLevel(getattr(logging, config.log_level))

file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setLevel(getattr(logging, config.log_level))

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

async def log_info(ctx, message: str, is_debug: bool = False):
    if is_debug:
        logger.info(message)
        
    if ctx:
        await ctx.info(message)
