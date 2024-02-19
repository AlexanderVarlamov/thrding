"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 12.02.2024
@time 12:25
"""
import time
from multiprocessing import Lock, SimpleQueue, Process, Queue, Event


def handler(elem):
    import time
    time.sleep(0.1)
    return elem + 1



def worker(lock: Lock, stor: SimpleQueue, event: Event) -> None:
    while True:
        if event.is_set:
            break
        with lock:
            elem = stor.get()
            if elem is None:
                event.set()
                break
            stor.put(handler(elem))

if __name__ == '__main__':
    start = time.perf_counter()
    lock = Lock()
    queue = SimpleQueue()
    event = Event()
    for n in range(10):
        queue.put(n)
    queue.put(None)
    processes = [Process(target=worker, args=(lock, queue, event)) for _ in range(3)]
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()

    while not queue.empty():
        print(queue.get())

    print(time.perf_counter() - start)