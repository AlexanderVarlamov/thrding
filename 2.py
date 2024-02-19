import queue
import threading
from queue import Queue


class CCD:
    def __init__(self, kwargs: dict):
        self.cat: str = kwargs.get('cat')
        self.union: bool = kwargs.get('union')
        self.cargo: dict = kwargs.get('cargo')
        self.id: int = kwargs.get('id')

    def __lt__(self, other):
        fast_cat = {'0201', '0202', '0203', '0204', '0205', '0206', '0207', '0208', '0209'}

        return (not self.union, self.cat not in fast_cat, self.id) < (
            not other.union, other.cat not in fast_cat, other.id)


main_queue = Queue(maxsize=30)
sup_queue = Queue()

from random import choice, randint
from itertools import count

count_gen = count(1)


def get_next_declar():
    for _ in range(5):
        new_dict = {
            "cat": "".join([str(randint(0, 9)) for _ in range(4)]),
            "union": choice([True, False]),
            "cargo": {},
            "id": next(count_gen)
        }
        yield new_dict
    else:
        yield None


def handler(elem):
    import time
    time.sleep(0.1)
    return True


def producer():
    for dct in get_next_declar():
        if dct is None:
            return
        try:
            main_queue.put(CCD(dct), timeout=0.01)
        except queue.Full:
            sup_queue.put(CCD(dct))


tw = 0.5
from datetime import datetime


def consumer(t_wait):
    while True:
        try:
            declar = main_queue.get(timeout=t_wait)
            print(declar.id)
        except queue.Empty:
            print(f"Empty {datetime.now()} thread = {threading.current_thread().name}")
            break


main_thread = threading.Thread(target=producer, name='prod_0')
cons_thread1 = threading.Thread(target=consumer, args=[tw], name='insp_1', daemon=True)

main_thread.start()
main_thread.join()
print(main_queue.qsize())
cons_thread1.start()
cons_thread1.join()