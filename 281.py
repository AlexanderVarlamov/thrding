"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 16.01.2024
@time 11:10
"""
import datetime
import threading
from itertools import count
from time import perf_counter
from typing import Callable


class TestWorker(threading.Thread):
    def __init__(self, task: Callable, permission: Callable, condition: threading.Condition):
        super().__init__()
        self.permission = permission
        self.task = task
        self.condition = condition

        stor_local = threading.local()
        stor_local.permission = False

    def make_work(self):  # основной метод выполняет задачу если получено условие
        with self.condition:
            start = perf_counter()
            tmp = self.condition.wait_for(predicate=self.permission, timeout=5)
            if tmp:
                self.task()  # выполняем задачу если разрешено
            else:
                # не выполняем задачу, просто логируем, что не дождались условия и выводим время
                print(f"escaping by timer with {threading.current_thread().name=}, {perf_counter() - start}")

    def run(self):
        self.make_work()


def task():
    print(f"working task with {threading.current_thread().name=}")


_count = count(1)
condition = threading.Condition()

stor_local = threading.local()
stor_local.permission = False

def permission():
    thread_name = threading.current_thread().name
    if hasattr(stor_local, 'allow_next_time',):
        return True
    else:
        if hasattr(stor_local, 'permission',) and stor_local.permission:
            stor_local.allow_next_time = True

        return False



tw_1 = TestWorker(task=task, permission=permission, condition=condition).start()

tw_2 = TestWorker(task=task, permission=permission, condition=condition).start()

print(str(datetime.datetime.now()))