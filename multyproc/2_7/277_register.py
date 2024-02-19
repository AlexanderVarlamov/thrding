from multiprocessing.managers import BaseManager
import multiprocessing
from queue import Queue
from time import perf_counter


if __name__ == "__main__":
    manager = BaseManager(address=("localhost", 50_000), authkey=b"123")
    manager.register("queue_results")
    manager.connect()
    print("connect_ok")
    print(f"client №0 started, process PID = {multiprocessing.current_process().pid}")
    queue_results = manager.queue_results()
    queue_results: Queue
    count = 0
    start_time = None
    while True:
        start_time = start_time or perf_counter()
        msg = queue_results.get()
        if msg is None:
            break
        count += 1
        print(msg)
    print(f"all done, count numbers = {count}")
    print(f"time execution = {perf_counter() - start_time}")