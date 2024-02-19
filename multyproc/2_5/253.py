"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 05.02.2024
@time 15:05
"""
import queue
import time
from random import uniform


def get_files():
    for file in ["logo.png", "bar.png", "phon.png", "box.png", "info.png", "front_logo.png", None]:
        time.sleep(uniform(0.05, 0.1))
        yield file
    time.sleep(60)


def image_processing(file: str) -> str:
    time.sleep(uniform(0.5, 0.7))  # эмуляция работы
    return f"{file} processed successfully"


#  Ваше решение:
from multiprocessing import Queue, Process


# напишите решение
# сформируйте список log_processing

class Producer(Process):
    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue
        pass

    def run(self) -> None:
        for file in get_files():
            if file is not None:
                self.queue.put(file)
            else:
                self.queue.put(file)
                break


class Consumer(Process):
    def __init__(self, files_queue: Queue, result_queue: Queue):
        super().__init__()
        self.files_queue = files_queue
        self.result_queue = result_queue

    def run(self) -> None:
        while True:
            new_file = self.files_queue.get()
            if new_file is not None:
                self.result_queue.put(image_processing(new_file))
            else:
                self.files_queue.put(None)
                break



if __name__ == '__main__':
    start = time.perf_counter()
    queue_files = Queue()
    result_queue = Queue()
    producer = Producer(queue_files)
    producer.start()
    consumers = [Consumer(queue_files, result_queue) for _ in range(3)]
    for cons in consumers:
        cons.start()

    for cons in consumers:
        cons.join()

    producer.terminate()
    producer.join()
    producer.close()

    log_processing = []
    while True:
        try:
            log_processing.append(result_queue.get(block=False))
        except queue.Empty as e:
            break

    print(log_processing)
    print(time.perf_counter()-start)