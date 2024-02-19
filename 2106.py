"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 18.01.2024
@time 14:50
"""
from time import sleep

import requests


sources = ["https://ya.ru",
           "https://www.bing.com",
           "https://www.google.ru",
           "https://www.yahoo.com",
           "https://mail.ru"]

def get_request_header(url: str):
    return requests.get(url).headers

sources = ["url_1",
           "url_2",
           "url_3",
           "url_4",
           "url_5"]


def get_request_header(url: str) -> str:
    if url == "url_1":
        sleep(0.8)
    if url == "url_2":
        sleep(0.9)
    if url == "url_3":
        sleep(1.4)
    if url == "url_4":
        sleep(1.8)
    if url == "url_5":
        sleep(1.6)
    return f"{url}-headers"

import concurrent.futures

headers_stor = {}

for source in sources:
    headers_stor.update({source: 'no_response'})


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = [executor.submit(get_request_header, source) for source in sources]
    task_done, _ = concurrent.futures.wait(results, timeout=1.5)
    for source, future in zip(sources, results):
        if future in task_done:
            headers_stor.update({source: future.result()})


print(*headers_stor.items(), sep='\n')
