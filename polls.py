"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 13.02.2024
@time 15:36
"""
import multiprocessing
import time


def task(args: list):
    args2 = map(lambda x: x * x * x, args)
    result = sum(args2)
    return result


if __name__ == '__main__':
    start = time.perf_counter()
    for _ in range(10):
        task(range(20000000))
    print(time.perf_counter() - start)

    start = time.perf_counter()

    with multiprocessing.Pool() as pool:
        results = pool.map_async(task, iterable=[range(20000000) for _ in range(10)])
        results.get()
    print(time.perf_counter() - start)
