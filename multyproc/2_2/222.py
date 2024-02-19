"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 30.01.2024
@time 16:32
"""
import multiprocessing
import random
import time


def worker(name: str):
    tm = random.uniform(0.1, 4)
    print(f"{name=} {tm=}")
    time.sleep(tm)
    print(name)


class CSVHandler(multiprocessing.Process):
    def __init__(self, files: list[str] | tuple[str] = None, worker: callable = None, timeout: int = 1):
        super().__init__()
        self.files = files
        self.worker = worker
        self.timeout = timeout
        self.context = multiprocessing.get_context()
        self.size = len(files)

    def run(self) -> None:
        processes = [self.context.Process(target=self.worker, args=(file,), daemon=True) for file in self.files]
        for proc in processes:
            proc.start()

        time.sleep(self.timeout)

        for i in range(self.size):
            if processes[i].is_alive():
                processes[i].terminate()
                processes[i].join()
                processes[i].close()
                print(f"{self.files[i]} processing timeout exceeded")


if __name__ == '__main__':
    filenames = ['file_1.csv', 'file_2.csv', 'file_3.csv', 'file_4.csv', 'file_5.csv',
                 'file_6.csv']  # список файлов CSV для обработки
    csv_worker = CSVHandler(filenames, worker)
    csv_worker.timeout = 2
    csv_worker.start()
