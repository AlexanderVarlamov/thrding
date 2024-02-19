"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 30.01.2024
@time 10:35
"""
import multiprocessing
import time

sources = ["2023_08.csv", "2023_07.csv", "2023_06.csv", "2023_05.csv", "2023_04.csv"]


def handler(file: str) -> None:
    """
    Функция обработки платежей
    """
    print('start')
    time.sleep(10)
    print('finish')


def main(t: int | float):
    prs = [multiprocessing.Process(target=handler, args=(arg,), daemon=True) for arg in sources]
    for pr in prs:
        pr.start()
    time.sleep(t)
    for pr in prs:
        pr.terminate()
        pr.join()
        pr.close()


if __name__ == '__main__':
    main(3)
