"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 12.02.2024
@time 16:39
"""
import multiprocessing
from multiprocessing import Queue, Process


def task(arg):
    import time
    time.sleep(0.1)
    print(f"ident={multiprocessing.current_process().ident}, {arg}")

def work(task, queue):
    while True:
        numb = queue.get()
        if numb is None:
            queue.put(None)
            break
        else:
            task(numb)

def pool(max_workers, task, args):
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    queue = Queue()
    for arg in args:
        queue.put(arg)
    queue.put(None)
    processes = [Process(target=work, args=(task, queue)) for _ in range(max_workers)]
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()


if __name__ == "__main__":
    args = [1, 2, 3, 4, 5, 6, 7]
    pool(max_workers=3, task=task, args=args)