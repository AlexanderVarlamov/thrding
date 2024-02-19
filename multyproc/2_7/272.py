from threading import Timer as dfsd
from multiprocessing import Process, Event

def work(*args, **kwargs):
    print('xxx')

class Timer(Process):
    def __init__(self, interval, function, args=None, kwargs=None):
        super().__init__()
        self.interval = interval
        self.function = function
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.event = Event()

    def run(self) -> None:
        self.event.wait(self.interval)
        if not self.event.is_set():
            self.function(*self.args, **self.kwargs)

    def cancel(self):
        self.event.set()


if __name__ == '__main__':
    proc = Timer(2, work)
    proc.start()
    proc.cancel()
    proc.join()