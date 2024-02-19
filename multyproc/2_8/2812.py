"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 13.02.2024
@time 16:21
"""
import time


def task(arg):
    time.sleep(arg / 3)
    return arg + arg


# Ваше решение
from multiprocessing.pool import Pool
from typing import Iterable, Callable


def main(func: Callable, iterable: Iterable, timeout: int) -> list:
    results_to_return = []
    tasks = []
    with Pool() as pool:
        for elem in iterable:
            tasks.append(pool.apply_async(func, (elem,)))
        time.sleep(timeout)
        for single_task in tasks:
            if single_task.ready():
                results_to_return.append(single_task.get())
            else:
                results_to_return.append("TimeoutError")
    return results_to_return
    # допишите код


if __name__ == '__main__':
    data = (1, 2, 12, 1)
    print(main(task, data, 1))
