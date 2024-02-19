"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 01.02.2024
@time 11:29
"""

from ctypes import c_double, Structure, c_char


def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")

from multiprocessing import Queue, Process
import queue as qu

class Encrypter(Process):
    # допишите определение класса
    def __init__(self, text, queue: Queue):
        super().__init__()
        self.text = text
        self.queue = queue



    def run(self) -> None:
        result, quality = crypto_utils(self.text)
        self.queue.put({result: (self.text, quality)})




# дополните код и выведите results на печать.
# не забудьте про точку входа!

if __name__ == '__main__':
    queue = Queue()
    processes = [Encrypter(text, queue) for text in text_blocks]
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    results = {}

    while True:
        try:
            res = queue.get(block=False)
            results.update(res)
        except qu.Empty:
            break

