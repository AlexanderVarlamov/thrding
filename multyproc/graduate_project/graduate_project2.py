import bisect
import csv
import logging
import multiprocessing
import os
import sys
import time
from collections import deque
from datetime import datetime
from multiprocessing import Process, Queue

from dateutil.relativedelta import relativedelta
from matplotlib import pyplot as plt

ticker_list = ['SBER', 'LKOH', 'GAZP', 'ROSN', 'ALRS']
start_invest_date = datetime(year=2014, month=7, day=1)
last_invest_date = datetime(year=2024, month=2, day=1)

logger = multiprocessing.get_logger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter(fmt="{asctime} {levelname} {processName} {threadName}  {message}", style='{')

fh = logging.FileHandler('info_log.log')
fh.setFormatter(formatter)
logger.addHandler(fh)

sh = logging.StreamHandler(stream=sys.stdout)
sh.setFormatter(formatter)
logger.addHandler(sh)


class CountPrice(Process):
    def __init__(self, ticker: str, investment_days: list[datetime], queue, per_month: int | float = 2000):
        super().__init__()
        self.ticker = ticker
        self.investment_days = deque(investment_days)
        self.queue = queue
        self.per_month = per_month
        self.div_filename = os.sep.join([ticker, 'dividends.csv'])
        self.prices_filename = os.sep.join([ticker, 'prices.csv'])
        self.dividends = {}
        self.prices = {}
        self.investments = []
        self.div_amount = None
        self.div_day = None
        self.current_amount_tmp = None
        self.div_fix = None
        self.day_to_fix = None
        self.current_amount = None
        self.when_are_dividends = None
        self.days_to_fix_divs = None
        self.days_to_evaluate = None
        self.start_investing = None
        self.current_day_to_invest = None
        self.day_price = None

    def run(self) -> None:
        start = time.perf_counter()
        self.fill_dividends_and_prices()
        self.fill_investments()
        self.queue.put(list(map(lambda x: (x[0], x[2]), self.investments)))
        end = time.perf_counter()
        logger.info(f"Data for {self.ticker} is evaluated successfully in {end - start} seconds")

    def fill_dividends_and_prices(self):
        with open(self.prices_filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    key = datetime.strptime(row[0], '%Y-%m-%d')
                except Exception as e:
                    logger.warning(f"Key {row[0]} for {self.ticker} will be ignored. Unable to convert to datetime")
                    logger.warning(e)
                    continue
                try:
                    value = float(row[1])
                except Exception as e:
                    logger.warning(f"{row[0]} value {row[1]} for {self.ticker} will be ignored. Unable to convert to "
                                   f"float")
                    logger.warning(e)
                    continue
                self.prices.update({key: value})

        with open(self.div_filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    key = datetime.strptime(row[0], '%Y-%m-%d')
                except Exception as e:
                    logger.warning(f"Key {row[0]} for {self.ticker} will be ignored. Unable to convert to datetime")
                    logger.warning(e)
                    continue
                try:
                    value = float(row[1])
                except Exception as e:
                    logger.warning(f"{row[0]} value {row[1]} for {self.ticker} will be ignored. Unable to convert to "
                                   f"float")
                    logger.warning(e)
                    continue
                self.dividends.update({key: value})

    def prepare_checkpoints(self):
        self.start_investing = self.investment_days.popleft()
        self.days_to_evaluate = sorted(filter(lambda x: x >= self.start_investing, self.prices.keys()))
        self.days_to_fix_divs = deque(sorted(self.dividends.keys()))
        self.when_are_dividends = self.evaluate_div_dates(self.days_to_evaluate)
        self.current_amount = 0
        self.current_day_to_invest = self.start_investing
        if self.days_to_fix_divs:
            self.day_to_fix = self.days_to_fix_divs.popleft()
        else:
            self.day_to_fix = last_invest_date + relativedelta(years=1000)
        self.div_fix = 0
        if self.when_are_dividends:
            self.div_day, self.div_amount = self.when_are_dividends.popleft()
        else:
            self.div_day, self.div_amount = last_invest_date + relativedelta(years=1000), 0

    def check_if_fix_dividends(self, day):
        if day >= self.day_to_fix:
            self.div_fix = self.current_amount
            if self.days_to_fix_divs:
                self.day_to_fix = self.days_to_fix_divs.popleft()
            else:
                self.day_to_fix += relativedelta(years=1000)

    def check_if_invest(self, day):
        if day >= self.current_day_to_invest:
            new_amount = self.per_month / self.day_price
            self.current_amount_tmp += new_amount
            if self.investment_days:
                self.current_day_to_invest = self.investment_days.popleft()
            else:
                self.current_day_to_invest += relativedelta(years=1000)

    def check_if_dividends_today(self, day):
        if day >= self.div_day:
            new_amount = (self.div_fix * self.div_amount) / self.day_price
            self.current_amount_tmp += new_amount
            if self.when_are_dividends:
                self.div_day, self.div_amount = self.when_are_dividends.popleft()
            else:
                self.div_day, self.div_amount = self.div_day + relativedelta(years=1000), 0

    def fill_investments(self):
        self.prepare_checkpoints()
        for day in self.days_to_evaluate:
            self.current_amount_tmp = self.current_amount
            self.day_price = self.prices[day]
            self.check_if_fix_dividends(day)
            self.check_if_invest(day)
            self.check_if_dividends_today(day)
            self.current_amount = self.current_amount_tmp
            self.investments.append((day, self.current_amount_tmp, self.current_amount * self.day_price))

    def evaluate_div_dates(self, trade_days) -> deque[tuple[datetime, float]]:
        days_to_return = []
        for day in self.dividends:
            index = bisect.bisect_left(trade_days, day)
            days_to_return.append((trade_days[index + 8], self.dividends[day]))
        return deque(days_to_return)


def generate_dates():
    current = start_invest_date
    dates = []
    while current < last_invest_date + relativedelta(months=1):
        dates.append(current)
        current = current + relativedelta(months=1)
    return dates


def total_investment_count(temp_queue: Queue, result_queue: Queue, num: int):
    results = {}
    already_processed = 0
    start = time.perf_counter()
    while already_processed < num:
        temp_results = temp_queue.get()
        for res in temp_results:
            key = res[0]
            if key in results:
                value = results[key]
                value += res[1]
            else:
                value = res[1]
            results.update({key: value})
        already_processed += 1

    result_queue.put(list(results.items()))
    logger.info(f"Данные по бирже посчитаны за {time.perf_counter() - start:.3f} секунд")


def evaluate_bank_investment(investment_days, monthly_amount, percent=0.07):
    cur = 0
    money = []
    for _ in investment_days:
        cur *= (percent / 12) + 1
        cur += monthly_amount
        money.append(cur)

    return money


if __name__ == '__main__':
    temp_queue = Queue()
    result_queue = Queue()
    investment_days = generate_dates()
    size = len(ticker_list)
    monthly_amount = 10000
    percent = 0.07
    processes = [CountPrice(ticker, investment_days, temp_queue, monthly_amount/size) for ticker in ticker_list]

    for proc in processes:
        proc.start()
    logger.info("Расчёт по тикерам запущен")

    res_proc = Process(target=total_investment_count, args=(temp_queue, result_queue, size))
    res_proc.start()

    fig, ax = plt.subplots()
    ax.set_xlabel('Время')
    ax.set_ylabel('Цена портфеля, рубли')
    ax.set_title(f"Сравнение банковских инвестиций под {percent*100:.1f}% и биржевых инвестиций")
    ax.grid(True)

    X, Y = investment_days, evaluate_bank_investment(investment_days, monthly_amount, percent)
    ax.plot(X, Y)

    stocks = result_queue.get(timeout=4)
    res_proc.join()

    for proc in processes:
        proc.join()

    X1 = [x[0] for x in stocks]
    Y1 = [x[1] for x in stocks]
    ax.plot(X1, Y1)

    plt.show()
    logger.info("Chart have drown successfully")
