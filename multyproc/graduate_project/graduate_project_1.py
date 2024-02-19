import concurrent.futures
import logging
import os
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from queue import Queue
from typing import List

import requests

ticker_list = ['SBER', 'LKOH', 'GAZP', 'ROSN', 'ALRS']

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="{asctime} {levelname} {processName} {threadName}  {message}", style='{')

fh = logging.FileHandler('info_log.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)

ready_queue = Queue()


@dataclass
class Scope:
    start: str | None = None
    end: str | None = None

    def from_timestamps(self, start: datetime, end: datetime):
        self.start = datetime.strftime(start, '%Y-%m-%d')
        self.end = datetime.strftime(end, '%Y-%m-%d')


def request_handling(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(str(e) + f" in {func.__name__}")

    return wrapper


def make_dir(ticker: str):
    os.makedirs(ticker, exist_ok=True)


def write_file(queue: Queue):
    while True:
        new_elem = queue.get(timeout=5)
        if new_elem is None:
            break
        else:
            ticker, filetype, message = new_elem
            line_message = map(lambda x: ','.join([str(elem) for elem in x]) + '\n', message)
            filepath = os.sep.join((ticker, filetype)) + '.csv'
            make_dir(ticker)
            with open(filepath, 'w') as file:
                file.writelines(line_message)
            queue.task_done()



def get_dates(ticker: str):
    url = f"http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{ticker}/dates.json"
    response = requests.get(url)
    response_dict = response.json()
    min_date = response_dict['dates']['data'][0][0]
    max_date = response_dict['dates']['data'][0][1]
    return min_date, max_date


@request_handling
def get_dividend_dates(ticker):
    url = f"http://iss.moex.com/iss/securities/{ticker}/dividends.json"
    response = requests.get(url)
    response_dict = response.json()
    dates = response_dict['dividends']['data']
    ready_queue.put((ticker, 'dividends', map(lambda x: (x[2], x[3]), dates)))
    logger.info(f"Dividend data for {ticker} received in {time.perf_counter() - start:.3f} seconds")


def generates_edges(first: str, last: str):
    first_date = datetime.strptime(first, '%Y-%m-%d')
    next_date = first_date + timedelta(days=99)
    last_date = datetime.strptime(last, '%Y-%m-%d')
    dates_array: List[Scope] = []
    while last_date >= next_date:
        if first_date > last_date:
            break
        scope = Scope()
        scope.from_timestamps(first_date, next_date)
        dates_array.append(scope)
        first_date = next_date + timedelta(days=1)
        maybe_next_date = first_date + timedelta(days=99)
        next_date = maybe_next_date if last_date > maybe_next_date else last_date

    return dates_array


@request_handling
def get_prices(args):
    ticker = args[0]
    scope = args[1]
    url = f'http://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/' + \
          f'securities/{ticker}.json?from={scope.start}&till={scope.end}'
    response = requests.get(url)
    return [[data[1], data[11]] for data in response.json()['history']['data']]


def collect_prices(ticker: str):
    start = time.perf_counter()

    min_date, max_date = get_dates(ticker)
    scopes: List[Scope] = generates_edges(min_date, max_date)
    prices_lst = []

    with concurrent.futures.ThreadPoolExecutor() as pool:
        results = pool.map(get_prices, [(ticker, scope) for scope in scopes])

    for res in results:
        prices_lst.extend(res)

    ready_queue.put((ticker, 'prices', prices_lst))
    logger.info(f"Data for {ticker} received in {(time.perf_counter() - start):.3f} seconds")


if __name__ == '__main__':
    start = time.perf_counter()
    file_writer = threading.Thread(target=write_file, args=(ready_queue,))
    file_writer.start()

    with concurrent.futures.ThreadPoolExecutor() as pool:
        futures = [pool.submit(collect_prices, ticker) for ticker in ticker_list] + \
                  [pool.submit(get_dividend_dates, ticker) for ticker in ticker_list]

    concurrent.futures.wait(futures, timeout=5)
    ready_queue.put(None)
    file_writer.join()
    logger.info(f"All done in {time.perf_counter() - start:.3f} second")
