import logging
from functools import wraps

config_log = {
    "level": logging.INFO,
    "filename": "log.txt",
    "filemode": "w",
    "format": "{processName}, {threadName}, {message}, {asctime}",
    "style": "{"
}

logging.basicConfig(**config_log)


def loger(func: callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(func.__name__)
        func(*args, **kwargs)

    return wrapper


@loger
def main(rr):
    print(rr)
    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')
    logging.critical('critical message')


if __name__ == '__main__':
    main(44)
