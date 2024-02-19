"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 14.02.2024
@time 9:47
"""
import traceback
from concurrent.futures import ProcessPoolExecutor


def crypto_utils(text: str) -> tuple[str, float]:
    import time
    from random import uniform
    time.sleep(uniform(0, 3))
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")

import concurrent.futures

results = {}
errors = {}


def crypto_handler(timeout: float | int = 2) -> None:
    with concurrent.futures.ProcessPoolExecutor() as executor:
        res = []
        for text in text_blocks:
            res.append(executor.submit(crypto_utils, text))

        concurrent.futures.wait(res, timeout)

        for rs, text in zip(res, text_blocks):
            try:
                proc = rs.result(0)
                result = proc[0]
                quality = proc[1]
                results.update({result: (text, quality)})
            except Exception as err:
                print(err)
                errors.update({text: traceback.format_exception_only(err)[0].strip()})


if __name__ == "__main__":
    crypto_handler(2)
    print(results)
    print(errors)
