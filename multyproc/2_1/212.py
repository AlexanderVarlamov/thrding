"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 30.01.2024
@time 13:23
"""
import multiprocessing
import typing
from concurrent.futures import ThreadPoolExecutor


def pool(request: list[typing.Callable], sources: list[str]):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for request_, source in zip(request, sources):
            executor.submit(request_, source)


def request_handler(request: list[typing.Callable], sources: list[str], timeout: int | float) -> None:
    pr = multiprocessing.Process(target=pool, args=(request, sources))
    pr.start()
    pr.join(timeout)
    pr.terminate()
    pr.close()
