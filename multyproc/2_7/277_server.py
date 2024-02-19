"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 12.02.2024
@time 16:11
"""
from multiprocessing.managers import BaseManager
import multiprocessing
from queue import Queue


def check_prime(number):
    d = 2
    while number % d != 0:
        d += 1
    return d == number


numbers = [2985001, 2985953, 2986129, 4465009, 4469923, 4469951, 446998,
           5885449, 5889887, 6985367, 6989657, 7648939, 7649801, 7648411,
           8335571, 8336599, 8339987, 9977581, 9978131, 9978607, 11981707,
           11981707, 11982721, 11984429, 13965059, 13966783, 13969859, 13969897,
           15380003, 15381101, 15382901, 15383477, 15383923, 15384293, 15384973]

if __name__ == "__main__":
    manager = BaseManager(address=("localhost", 50_000), authkey=b"123")
    queue_number = Queue()
    queue_results = Queue(len(numbers))
    manager.register("queue_number", callable=lambda: queue_number)
    manager.register("queue_results", callable=lambda: queue_results)
    # manager.register("check_prime", callable=check_prime)
    for n in numbers:
        queue_number.put(n)
    server = manager.get_server()
    print(f"server started, process PID = {multiprocessing.current_process().pid}")
    print(f"count numbers = {queue_number.qsize()}")
    server.serve_forever()