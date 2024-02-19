"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 17.01.2024
@time 17:52
"""
import threading
from typing import Callable


class HubHendler:
    def __init__(self, n: int, task: Callable, n_threads: int):
        self.n = n
        self.task = task
        self.n_threads = n_threads
        self.semaphore = threading.Semaphore(n)

    def start_hub(self):
        threads = []
        for _ in range(self.n_threads):
            threads.append(threading.Thread(target=self.run_task))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def run_task(self):
        self.semaphore.acquire(blocking=True)
        self.task()
        self.semaphore.release()

