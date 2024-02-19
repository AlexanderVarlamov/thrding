import time
from multiprocessing import Pool
from typing import Callable, Iterable


def task(i):
    time.sleep(i)
    if i == 1:
        raise ValueError("Ops, ValueError")
    return i


class WaitPool:
    def __init__(self, func: Callable, args: Iterable):
        self.func = func
        self.args = args
        self.success = []
        self.failed = []
        self.tasks = []
        self.pool = Pool()

    def start(self):
        for elem in self.args:
            self.tasks.append(self.pool.apply_async(self.func, (elem,)))

    def wait(self):
        for tsk in self.tasks:
            if tsk.ready() and tsk.successful():
                self.success.append(tsk)
            else:
                self.failed.append(tsk)

        return self.success, self.failed

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.terminate()
        self.pool.join()
        self.pool.close()
        pass


if __name__ == "__main__":
    args = (0.5, 1, 1.1, 2.2, 3.3, 1.2, 1.4)

    with WaitPool(task, args) as pool:
        pool.start()
        time.sleep(2)
        done, not_done = pool.wait()

    print(len(done), len(not_done))  # 4, 3

    for d in done:
        print(d.get())
    try:
        not_done[0].get()
    except ValueError as err:
        print(err)
