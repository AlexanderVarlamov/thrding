"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 14.02.2024
@time 15:42
"""
import concurrent.futures
import multiprocessing
import random
import time
from concurrent.futures import Future


# дополните код
def get_image(url: str) -> str:
    # print(f"{multiprocessing.current_process().ident}")
    time.sleep(random.random())
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

def save(file: Future[str]):
    res = file.result()
    save_image(res)

def process(file):
    return image_processing(get_image(file))

def group_image_processing(file_source: str) -> None:
    # Получите urls из file_source
    with open(file_source, 'r') as file:
        lines = map(lambda l: l.strip(), file.readlines())
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for line in lines:
            future = executor.submit(process, line)
            future.add_done_callback(save)


if __name__ == '__main__':
    group_image_processing('urls')
    print('all')
