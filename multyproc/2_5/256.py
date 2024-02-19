"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 05.02.2024
@time 15:05
"""
import time
from random import uniform


def get_files():
    for file in ["logo.png", "bar.png", "phon.png", "box.png", "info.png", "front_logo.png"]:
        time.sleep(uniform(0.05, 0.1))
        yield file
    time.sleep(10)


def image_processing(file: str) -> str:
    time.sleep(uniform(0.5, 0.7))  # эмуляция работы
    return f"{file} processed successfully"


#  Ваше решение:
from multiprocessing import Process, SimpleQueue
from multiprocessing import JoinableQueue
import queue
# напишите решение
# сформируйте список log_processing

class Producer(Process):
    def __init__(self, queue: JoinableQueue):
        super().__init__(daemon=True)
        self.queue = queue
        pass

    def run(self) -> None:
        for file in get_files():
            self.queue.put(file)


class Consumer(Process):
    def __init__(self, files_queue: JoinableQueue, result_queue: SimpleQueue):
        super().__init__(daemon=True)
        self.files_queue = files_queue
        self.result_queue = result_queue

    def run(self) -> None:
        while True:
            try:
                new_file = self.files_queue.get()
                self.result_queue.put(image_processing(new_file))
                self.files_queue.task_done()
            except queue.Empty as e:
                break


if __name__ == '__main__':
    start = time.perf_counter()
    queue_files = JoinableQueue()
    result_queue = SimpleQueue()
    producer = Producer(queue_files)
    producer.start()

    consumers = [Consumer(queue_files, result_queue) for _ in range(3)]
    for cons in consumers:
        cons.start()
    producer.join()

    queue_files.join()

    for cons in consumers:
        cons.terminate()
        cons.join()
        cons.close()
    log_processing = []

    while not result_queue.empty():
        res = result_queue.get()
        log_processing.append(res)



    print(log_processing)
    print(time.perf_counter()-start)
