"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 19.01.2024
@time 11:57
"""
import os
import threading
from datetime import datetime

import matplotlib.pyplot as plt

import csv

current_date = (datetime.now()).strftime('%d.%m.%y')
dir_name = os.sep.join(['csv', current_date])


class NormThread(threading.Thread):
    def __init__(self, filename, semaphore):
        super().__init__()
        self.filename = filename
        self.semaphore = semaphore
        self.normalized = []

    def run(self):
        with self.semaphore:
            data = self.read_ticker_data()
            base_value = data[0][1]
            for point in data:
                x, y = point
                y_norm = (y / base_value) * 100
                point.append(y_norm)
            self.normalized = data
            self.write_normalized_data()

    def read_ticker_data(self):
        result = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                result.append([row[0], float(row[1])])

        return result

    def write_normalized_data(self):
        if self.normalized:
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerows(self.normalized)


def make_coordinates(filename):
    x, y = [], []
    with open(filename, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            x.append(datetime.fromtimestamp(float(row[0])))
            y.append(float(row[2]))

    return x, y


def main():
    filenames = [os.sep.join((dir_name, filename)) for filename in os.listdir(dir_name)]
    semaphore = threading.Semaphore(3)
    threads = [NormThread(filename, semaphore) for filename in filenames]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    fig, ax = plt.subplots()
    ax.set_xlabel('Время')
    ax.set_ylabel('Цена в условных единицах')
    ax.set_title("Динамика цен на акции")
    ax.grid(True)
    for filename in filenames:
        X, Y = make_coordinates(filename)
        ax.plot(X, Y, label=filename.split(os.sep)[2])
        ax.legend()

    plt.show()


if __name__ == '__main__':
    main()
