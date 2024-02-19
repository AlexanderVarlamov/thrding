"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 18.01.2024
@time 15:18
"""
import concurrent.futures

sources = [1, 2, 3, 4, 5]


def worker(arg):
    if arg == 4:
        raise ValueError('пришло 4')
    else:
        return arg ** 2


def post_worker(future):
    exception = future.exception()
    if exception is not None:
        print(exception)
    else:
        print(f'{future.results()} saved')


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(worker, arg) for arg in sources]
    for future in futures:
        future.add_done_callback(post_worker)
