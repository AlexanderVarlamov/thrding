"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 12.02.2024
@time 17:11
"""
import multiprocessing
import time
from multiprocessing import Queue, Process
from random import uniform
from typing import Callable


def task(arg):
    time.sleep(uniform(0, 1))
    return multiprocessing.current_process().ident, arg


class SimplePool:
    def __init__(self, max_workers=None):
        self.max_workers = max_workers if max_workers else multiprocessing.cpu_count()
        self.arg_queue = Queue()
        self.res_queue = Queue()

    def map(self, task: Callable, args=None):
        for i, arg in enumerate(args):
            self.arg_queue.put((i, arg))
        self.arg_queue.put(None)

        processes = [Process(target=SimplePool._worker,
                             args=(task, self.arg_queue, self.res_queue)) for _ in range(self.max_workers)]

        for proc in processes:
            proc.start()

        for proc in processes:
            proc.join()

        return self._process_result()

    @staticmethod
    def _worker(task, arg_queue: Queue, res_queue: Queue):
        while True:
            from_queue = arg_queue.get()
            if from_queue is None:
                arg_queue.put(None)
                break
            else:
                i, elem = from_queue
                res_queue.put((i, task(elem)))

    def _process_result(self):
        result = []
        while not self.res_queue.empty():
            result.append(self.res_queue.get())

        result.sort(key=lambda x: x[0])
        return list(map(lambda x: x[1], result))


if __name__ == "__main__":
    args = [1, 2, 3, 4, 5, 6, 7]
    my_pool = SimplePool(3)
    for _id, v in my_pool.map(task=task, args=args):
        print(f"ident={_id}, {v}")
