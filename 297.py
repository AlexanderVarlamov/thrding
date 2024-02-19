"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 18.01.2024
@time 10:39
"""
import random
import time


def finalizer():
    print("STAGE #1.py ALL DONE!")


def task_st_1():
    time.sleep(random.uniform(0, 1))
    print(f"stage #1.py done by {threading.current_thread().name}")


def task_st_2():
    time.sleep(random.uniform(0, 1))
    print(f"stage #2 done by {threading.current_thread().name}")


#  Ваше решение:

import threading

barrier = threading.Barrier(4, action=finalizer)


def work(barrier):
    task_st_1()
    barrier.wait()
    task_st_2()


threads = []
for _ in range(4):
    threads.append(threading.Thread(target=work, args=(barrier,)))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
