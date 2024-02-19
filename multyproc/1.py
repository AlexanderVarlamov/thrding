import time
from multiprocessing.pool import Pool
from time import sleep


def task(x):
    sleep(x/2)
    return x*x


if __name__ == '__main__':
    print("A")
    with Pool(5) as pool:
        start = time.perf_counter()
        pool: Pool
        data = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        rez = pool.map(task, data)
        print(rez)
        print(time.perf_counter()-start)

    print("B")
    with Pool(5) as pool:
        start = time.perf_counter()
        pool: Pool
        data = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        for rez in pool.imap(task, data):
            print(rez)
            print(time.perf_counter() - start)

    print("C")
    with Pool(5) as pool:
        start = time.perf_counter()
        pool: Pool
        data = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        rez = pool.map_async(task, data)
        print(rez)
        print(time.perf_counter() - start)

    print("D")
    with Pool(5) as pool:
        start = time.perf_counter()
        pool: Pool
        data = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        for rez in pool.imap_unordered(task, data):
            print(rez)
            print(time.perf_counter() - start)