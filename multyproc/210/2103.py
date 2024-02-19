"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 15.02.2024
@time 10:42
"""
import logging
from functools import wraps

# дополните код
config_log = {
    "level": logging.INFO,
    "filename": "log.txt",
    "format": "{processName}, {threadName}, {asctime}, {__name__} => {message}"
}

logging.basicConfig(**config_log)

def loger(func: callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(func.__name__)
        func(*args, **kwargs)

    return wrapper