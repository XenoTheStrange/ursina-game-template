#!/usr/bin/python3

import sys
import logging
import traceback

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
log = logging
log.debug("Logger Initialized")

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            log.error(f"In: {func.__name__}()\nException: {error.__repr__() + ''.join(traceback.format_tb(error.__traceback__))}\n")
            # Optionally, you can raise the error again or return a default value
            return None #or raise
    return wrapper
