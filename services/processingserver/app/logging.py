import logging
import sys
from logging import Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

from app.config import settings

# Inspired from https://github.com/encode/starlette/issues/864#issuecomment-1047143865
def setup_logger():
    formatter = Formatter(settings.logging.FORMAT)

    # Stream handler
    stream_handler_out = StreamHandler(stream=sys.stdout)
    stream_handler_out.setFormatter(formatter)

    # Stream handler
    stream_handler_err = StreamHandler(stream=sys.stderr)
    stream_handler_err.setFormatter(formatter)

    # File handler
    file_handler = RotatingFileHandler(
        filename=settings.logging.LOG_FILENAME,
        maxBytes=settings.logging.MAX_BYTES,
        backupCount=settings.logging.BACKUP_COUNT,
    )
    file_handler.setFormatter(formatter)

    # Logger uvicorn.error
    logger = logging.getLogger("uvicorn.error")
    logger.propagate = False
    logger.setLevel(settings.logging.LEVEL)
    logger.handlers.clear()
    logger.addHandler(stream_handler_err)
    logger.addHandler(file_handler)

    # Logger uvicorn.access
    logger = logging.getLogger("uvicorn.access")
    logger.propagate = False
    logger.setLevel(settings.logging.LEVEL)
    logger.handlers.clear()
    logger.addHandler(stream_handler_out)
    logger.addHandler(file_handler)

    # App logger
    app_logger = logging.getLogger("bioformats_imageserver")
    app_logger.setLevel(settings.logging.LEVEL)
    app_logger.handlers.clear()
    app_logger.addHandler(stream_handler_out)
    app_logger.addHandler(file_handler)

    return app_logger
