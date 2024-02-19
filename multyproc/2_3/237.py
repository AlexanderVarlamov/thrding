"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 01.02.2024
@time 11:29
"""


def crypto_utils(text: str) -> str:
    if text.startswith("a"):
        return "aaa45678"
    if text.startswith("b"):
        return "bbb45678"


text_blocks = ("allocation", "bombshell")

import multiprocessing


class Encrypter(multiprocessing.Process):
    # допишите определение класса
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.result = multiprocessing.Array('c', b"********")

    def run(self) -> None:
        res = crypto_utils(self.text)
        self.result.value = res.encode()


# дополните код и выведите results на печать.
# не забудьте про точку входа!

if __name__ == '__main__':
    processes = [Encrypter(text) for text in text_blocks]
    for proc in processes:
        proc.start()

    for proc in processes:
        proc.join()

    results = {proc.result[:].decode(): text for proc, text in zip(processes, text_blocks)}
    print(results)
