# app/utils/decorators.py

import functools
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgentLogger")

def handle_errors(default_return=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Error in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator
