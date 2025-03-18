import logging

logging.basicConfig(
    filename="app_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",  # Log message format
)
logger = logging.getLogger(__name__)
