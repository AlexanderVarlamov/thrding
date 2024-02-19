import multiprocessing
import time


def task():
    res = 1
    for i in range(1, 100000):
        res *= i


def main():
    start = time.perf_counter()
    processes = []
    for _ in range(3):
        # pr = multiprocessing.Process(target=task)
        # pr.start()
        # pr.join()
        processes.append(multiprocessing.Process(target=task))
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

    print(time.perf_counter() - start)


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()
