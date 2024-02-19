"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 12.02.2024
@time 16:11
"""
from multiprocessing.managers import BaseManager
import multiprocessing

def check_prime(number):
    d = 2
    while number % d != 0:
        d += 1
    return d == number

if __name__ == "__main__":
    manager = BaseManager(address=("localhost", 50_000), authkey=b"123")
    manager.register("queue_number")
    manager.register("queue_results")
    manager.register("check_prime")
    manager.connect()
    print("connect_ok")
    print(f"client №2 started, process PID = {multiprocessing.current_process().pid}")
    queue_number = manager.queue_number()
    queue_results = manager.queue_results()

    while not queue_number.empty():
        number = queue_number.get()
        is_pr = check_prime(number)
        msg = f"{number=} {'is' if is_pr else 'is not'} prime"
        queue_results.put(msg)
        print(msg)
    queue_results.put(None)