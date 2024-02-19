"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 30.01.2024
@time 10:55
"""
import multiprocessing
import time
from typing import Callable, Iterable


def task1(*args):
    print("Start task 1.py")
    time.sleep(1)
    print(args)
    print("finish task 1.py")


def task2(*args):
    print("Start task 2_1")
    time.sleep(2)
    print(args)
    print("finish task 2_1")


def task3(*args):
    print("Start task 2_2")
    time.sleep(3)
    print(args)
    print("finish task 2_2")


def task4(*args):
    print("Start task 4")
    time.sleep(20)
    print(args)
    print("finish task 4")


def handle_tasks(tasks: Iterable[Callable], args: Iterable):
    prs = [multiprocessing.Process(target=task, args=arg, daemon=True) for task, arg in zip(tasks, args)]
    for pr in prs:
        pr.start()
    for pr in prs:
        pr.join()


def parallel_handler(tasks: Iterable[Callable], args: Iterable, timeout=None):
    pr = multiprocessing.Process(target=handle_tasks, args=(tasks, args))
    pr.start()
    pr.join(timeout)
    pr.kill()



if __name__ == "__main__":
    parallel_handler((task1, task2, task3, task4),
                     ((1.5, 1), (1.6, 2), (3, "BFG", "DOOM"), (4, 4, 4.01, 0.9)), timeout=2.2)
