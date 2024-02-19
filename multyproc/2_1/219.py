"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 30.01.2024
@time 10:35
"""
import multiprocessing

sources = ["2023_08.csv", "2023_07.csv", "2023_06.csv", "2023_05.csv", "2023_04.csv"]


def handler(file: str) -> None:
    """
    Функция обработки платежей
    """
    ...


def main():
    prs = [multiprocessing.Process(target=handler, args=(arg,)) for arg in sources]
    for pr in prs:
        pr.start()

    for pr in prs:
        pr.join()


if __name__ == '__main__':
    main()
