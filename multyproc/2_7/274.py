
from multiprocessing import Queue, Semaphore


def worker(elem_queue: Queue, result_queue: Queue, lock: Semaphore) -> None:
    while True:
        with lock:
            elem = elem_queue.get()
            if elem is None:
                elem_queue.put(elem)
                break
            result_queue.put(handler(elem))

if __name__ == "__main__":
    elem_queue = Queue()
    result_queue = Queue()
    obj_lock = Semaphore(3)
