"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 01.02.2024
@time 10:26
"""
import multiprocessing
from functools import reduce
from random import randint

def task(*args) -> float:
    return sum(args) + randint(1, 10) + 0.1


class MyProcess(multiprocessing.Process):
    def __init__(self, target=None, args=None):
        super().__init__()
        self.target = target
        self.args = args
        self.result = multiprocessing.Value('d', 0.0)

    def run(self):
        result = self.target(*self.args)
        self.result.value = result


if __name__ == '__main__':
    processes = [MyProcess(task, arg) for arg in ((2, 4), (2, 4), (2, 4))]
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

    print(*map(lambda proc: proc.result.value, processes))
    res = reduce(lambda x, y: x+y, map(lambda proc: proc.result.value, processes))
    print(res)
