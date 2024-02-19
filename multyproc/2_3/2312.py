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

import multiprocessing
from multiprocessing import shared_memory
import struct


class Encrypter(multiprocessing.Process):
    # допишите определение класса
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.memory = shared_memory.SharedMemory(size=16, create=True)



    def run(self) -> None:
        memory = self.memory.buf
        raw_result = crypto_utils(self.text)
        memory[:8] = raw_result[0].encode()
        memory[8:16] = struct.pack('<d', raw_result[1])



# дополните код и выведите results на печать.
# не забудьте про точку входа!

if __name__ == '__main__':
    processes = [Encrypter(text) for text in text_blocks]
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    results = {}

    for proc, text in zip(processes, text_blocks):
        result = proc.memory.buf[0:8].tobytes().decode()
        quality = struct.unpack('d', proc.memory.buf[8:].tobytes())[0]
        results.update({result: (text, quality)})

    print(results)
