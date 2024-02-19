"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 01.02.2024
@time 11:29
"""

from ctypes import c_double, Structure, c_char
from multiprocessing.managers import SharedMemoryManager


def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")

import multiprocessing
from multiprocessing import shared_memory


class Encrypter(multiprocessing.Process):
    # допишите определение класса
    def __init__(self, text, manager):
        super().__init__()
        self.text = text
        self.memory = manager.ShareableList(['1'*8, '2'*8])



    def run(self) -> None:
        raw_result = crypto_utils(self.text)
        self.memory[0] = raw_result[0]
        self.memory[1] = raw_result[1]



if __name__ == '__main__':
    shm = SharedMemoryManager()
    with shm:
        processes = [Encrypter(text, shm) for text in text_blocks]
        for proc in processes:
            proc.start()

        for proc in processes:
            proc.join()

        results = {}

        for proc, text in zip(processes, text_blocks):
            result = proc.memory[0]
            quality = proc.memory[1]
            results.update({result: (text, quality)})

    print(results)
