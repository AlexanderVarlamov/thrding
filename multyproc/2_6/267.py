"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 07.02.2024
@time 16:37
"""
import time
from multiprocessing import Process
from multiprocessing.connection import Connection, Pipe


# создайте целевую функцию дочернего процесса
# создайте канал
# создайте и запустите один дочерний процесс
# передайте через канал дочернему процессу объекты для расчета и
# получите ответ для формирования списка результата result
# ! придумайте защиту от зависания !

def get_obj():
    for i in range(10):
        yield i

def worker(data):
    import random as r
    time.sleep(r.uniform(0.1, 0.4))
    return data, 8, 4.523


def child_func(con: Connection):
    while True:
        con.send(worker(con.recv()))


if __name__ == '__main__':
    parent_con, child_con = Pipe()
    result = []
    child_proc = Process(target=child_func, args=(child_con,), daemon=True)
    child_proc.start()

    for data in get_obj():
        parent_con.send(data)
        if parent_con.poll(timeout=0.3):
            result.append(parent_con.recv())
        else:
            break

    child_proc.terminate()
    child_proc.join()
    child_proc.close()

    print(result)