import logging


def setup_logging():
    """Настройка логирования."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    return logger


logger = setup_logging()
