"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 01.02.2024
@time 10:46
"""
import multiprocessing
import random
from typing import Callable


def min_max_avg(arg):
    numbers = [0] * 100
    for i in range(100):
        numbers[i] = random.randint(1, 100)
    numbers.append(arg)
    mx = max(numbers)
    mn = min(numbers)
    av = int(sum(numbers) / len(numbers)+1)

    return mn, mx, av


class MinMaxAvr(multiprocessing.Process):
    def __init__(self, target: Callable, args: int | float):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Array('i', 3)

    def run(self):
        self.result[0], self.result[1], self.result[2] = self.target(*self.args)


if __name__ == '__main__':
    processes = [MinMaxAvr(min_max_avg, arg) for arg in (-1, 3, 145, 5)]
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

    for proc in processes:
        print(f"min is {proc.result[0]} max is {proc.result[1]} avg is {proc.result[2]}")
