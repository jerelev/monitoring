from functools import wraps
import logging
import time

log = logging.getLogger(__name__)

def measure_latency(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        log.info(f'enter function: {func.__name__}')
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        duration = end-start
        log.info(f'exit function. time spent in function: {func.__name__}: {duration}')
        return result
    return wrapper