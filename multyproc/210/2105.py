"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 15.02.2024
@time 11:40
"""
import concurrent.futures
import logging
import multiprocessing
import time
import random
from functools import wraps

# измените код, добавьте логирование ошибок в файл log_errors.txt

config_log = {
    "level": logging.INFO,
    "filename": "log.txt",
    "format": "{processName}, {threadName}, {asctime}, {__name__} => {message}"
}

logger = multiprocessing.get_logger()
logger.setLevel(logging.ERROR)
fh = logging.FileHandler("log_errors.txt")
fh.setFormatter(logging.Formatter(fmt="{processName}, {asctime}, {message}", style='{'))
logger.addHandler(fh)


def get_image(url: str) -> str:
    # print(f"{multiprocessing.current_process().ident}")
    seed = random.random()
    time.sleep(seed)
    if seed > 0.8:
        raise ValueError(str(seed) + __name__)
    return url + 'g'


def image_processing(file: str) -> str:
    print(file)
    # print(f"{multiprocessing.current_process().ident}")
    time.sleep(random.random())
    return file + 'p'


def save_image(file: str) -> None:
    print(file)
    time.sleep(random.random())
    # print(f"{multiprocessing.current_process().ident}")
    print(file+'s')

def handler(url: str) -> str:
    try:
        file = get_image(url)
    except Exception as e:
        logger.error(f"{get_image.__name__}, {e}")
        return
    try:
        return image_processing(file)
    except Exception as e:
        logger.error(f"{image_processing.__name__}, {e}")


def callback_save(future: concurrent.futures.Future) -> None:
    new_file = future.result()
    try:
        save_image(new_file)
    except Exception as e:
        logger.error(f"{save_image.__name__}, {e}")

def group_image_processing(file_source: str) -> None:
    with open(file_source) as file:
        urls = file.read().split()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for url in urls:
            future = executor.submit(handler, url)
            future.add_done_callback(callback_save)


if __name__ == '__main__':
    group_image_processing('urls')
    print('all')
