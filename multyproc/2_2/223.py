"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 31.01.2024
@time 9:33
"""
import multiprocessing
import threading
from typing import Callable


def task(*arg):
    print(arg)
    import time
    time.sleep(sum(arg))
    print(f"{arg} done")


class ParallelExecuter:
    def __init__(self, tasks: list[Callable] | tuple[Callable], args: list | tuple, timeout: int | float = 1):
        self.log = []
        self.timeout = timeout
        self.tasks = tasks
        self.args = args
        self.context = multiprocessing.get_context()
        self.length = len(self.tasks)
        self.processes = []

    def execute(self):
        self.processes = [self.context.Process(target=task, args=arg) for task, arg in zip(self.tasks, self.args)]
        for proc in self.processes:
            proc.start()
        main_thread = threading.Timer(self.timeout, function=self.clear_processes)
        main_thread.start()
        main_thread.join()


    def clear_processes(self):
        for i in range(self.length):
            if self.processes[i].is_alive():
                self.log.append(f"{self.tasks[i].__name__} processing timeout exceeded")
                self.processes[i].terminate()
                self.processes[i].join()
                self.processes[i].close()
            else:
                self.log.append(f"{self.tasks[i].__name__} completed successfully")


if __name__ == '__main__':
    executor = ParallelExecuter(tasks=[task, task, task, task], args=((0.8, 0.1), (1, -0.1), (2,), (0.8, )))
    executor.execute()
    print(executor.log)
