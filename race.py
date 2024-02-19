"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 15.01.2024
@time 17:48
"""
import threading
import time

x = 0
lock = threading.Lock()

def add_one():
    global x
    for _ in range(500):
        lock.acquire()
        local_x = x
        local_x += 1
        time.sleep(0)
        x = local_x
        lock.release()

th1 = threading.Thread(target=add_one)
th2 = threading.Thread(target=add_one)
th3 = threading.Thread(target=add_one)

th1.start()
th2.start()
th3.start()
th1.join()
th2.join()
th3.join()

print(x)
