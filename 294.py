"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 17.01.2024
@time 17:49
"""

import threading
import time

_bl, _tm, _vl = False, 0, 0


def task(sema: threading.Semaphore, text):
    s = sema.acquire(blocking=_bl, timeout=_tm)
    print(f"thread id = {threading.current_thread().ident} print {text}, acquire={s}, value= {sema._value}")
    time.sleep(1)
    sema.release()


semaphore = threading.Semaphore(_vl)

thr = []
for i in range(20):
    thr.append(threading.Thread(target=task, args=(semaphore, i)))
for t in thr:
    t.start()

for t in thr:
    t.join()

print(semaphore._value)