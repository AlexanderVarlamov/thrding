"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 13.02.2024
@time 14:40
"""
import time
import traceback


def task(a, b, c):
    if not isinstance(a, int | float):
        raise TypeError("not a number!")
    time.sleep(a / 10)
    return sum((a, b, c))


def data_gen():
    yield 1, 2, 3
    yield 10, 20, 30
    yield "a", "b", "c"
    yield 1.0, 2.0, 3.0


# Ваше решение

from multiprocessing.pool import Pool


def err_callback(err):
    print(err)


if __name__ == '__main__':
    results = []
    to_print = []
    with Pool() as pool:
        for args in data_gen():
            results.append(pool.apply_async(task, args))

        for res in results:
            try:
                xx = res.get()
                to_print.append(xx)
            except Exception as e:
                to_print.append(e)

    print(to_print)