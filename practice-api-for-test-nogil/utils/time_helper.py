import time
from loguru import logger
from typing import Callable
from datetime import datetime, timezone, timedelta

tz_tw = timezone(timedelta(hours=8), "Asia/Taipei")


# def time_taken() -> Callable:
#     def decorator(func: Callable) -> Callable:
#         def wrapper(*args, **kwargs):
#             start = time.time()
#             result = func(*args, **kwargs)
#             end = time.time()
#             print(f"Time taken by {func.__name__}: {end - start}")
#             return result

#         return wrapper

#     return decorator


def time_taken(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"Time taken by {func.__name__}: {(end - start)*1000:.2f} ms")
        return result

    return wrapper


def utc_now() -> Callable:
    return datetime.now(timezone.utc)
