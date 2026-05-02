# src/logger.py
import logging
from src.config import LOG_LEVEL

_configured = False


def get_logger(name: str = "agent") -> logging.Logger:
    """Returns a configured logger. Safe to call multiple times."""
    global _configured

    logger = logging.getLogger(name)

    if not _configured:
        root = logging.getLogger()
        root.setLevel(LOG_LEVEL)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        handler.setFormatter(formatter)
        root.addHandler(handler)
        _configured = True

    return logger
