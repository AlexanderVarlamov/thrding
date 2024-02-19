"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 19.01.2024
@time 11:57
"""
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from queue import Queue
from threading import Thread

import requests

tickers = ['AAPL', 'MSFT', 'AMZN', 'NVDA', 'TSLA', 'GOOGL', 'META', 'BRK-B', 'UNH', 'JPM']
start_date = '01.01.20'
current_date = (datetime.now()).strftime('%d.%m.%y')
dir_name = os.sep.join(['csv', current_date])

line_queue = Queue()


def get_history_data(kwargs):
    """
    Получает исторические данные для указанного тикера актива.

    :param ticker: str, тикер актива.
    :param start_date: str, дата начала периода в формате 'дд.мм.гг'.
    :param end_date: str, дата окончания периода в формате 'дд.мм.гг'.
    :param interval: str, интервал времени (неделя, день и т.д.) (необязательный, по умолчанию '1wk' - одна неделя).
    :return: str, JSON-строка с историческими данными.
    """
    ticker = kwargs.get('ticker', None)
    start_date = kwargs.get('start_date', '01.01.2023')
    end_date = kwargs.get('end_date', '01.01.2023')
    interval = kwargs.get('interval', '1wk')
    per2 = int(datetime.strptime(end_date, '%d.%m.%y').replace(tzinfo=timezone.utc).timestamp())
    per1 = int(datetime.strptime(start_date, '%d.%m.%y').replace(tzinfo=timezone.utc).timestamp())
    params = {"period1": str(per1), "period2": str(per2),
              "interval": interval, "includeAdjustedClose": "true"}
    user_agent_key = "User-Agent"
    user_agent_value = "Mozilla/5.0"
    headers = {user_agent_key: user_agent_value}
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
    response = requests.get(url, headers=headers, params=params)
    return response.json()


def pipeline(kwargs: dict):
    data_to_write = {}
    try:
        result = get_history_data(kwargs)
        data_to_write = process_json_to_csv(result)
    except TimeoutError as e:
        print(str(e).center(20, '-'))
        pass
    line_queue.put(data_to_write)


def process_json_to_csv(jsn: dict) -> str:
    result = {}
    try:
        adjclose = ((jsn['chart']['result'][0])["indicators"]["adjclose"][0])["adjclose"]
        adjclose_str = map(str, adjclose)
        stock_name = (jsn['chart']['result'][0])["meta"]["symbol"]
        timestamps = (jsn['chart']['result'][0])['timestamp']
        timestamps_str = map(str, timestamps)
        result = {'ticker': stock_name, 'data': list(zip(timestamps_str, adjclose_str))}
    except Exception as e:
        print(str(e).center(20, '-'))
        pass
    return result


def write_result_to_file():
    while True:
        data_to_write = line_queue.get(timeout=10)
        if data_to_write:
            filename = os.sep.join([dir_name, data_to_write['ticker']])
            points = [','.join(point) for point in data_to_write['data']]
            data = '\n'.join(points)
            with open(filename, mode='w') as file:
                file.write(data)
            line_queue.task_done()


def main():
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    args_to_get_data = [{'ticker': ticker, 'start_date': start_date, 'end_date': current_date} for ticker in tickers]
    filewriter = Thread(target=write_result_to_file, daemon=True)
    filewriter.start()
    with ThreadPoolExecutor(max_workers=len(tickers)) as executor:
        executor.map(pipeline, args_to_get_data, timeout=3)

    line_queue.join()


if __name__ == '__main__':
    main()
