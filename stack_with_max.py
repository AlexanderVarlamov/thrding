"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 13.02.2024
@time 11:36
"""
from collections import deque


class StackWithMax:
    def __init__(self):
        self.numbers = deque()
        self.maxes = deque()
        self._current_max = -float('inf')

    def put(self, number):
        if number >= self._current_max:
            self.maxes.appendleft(number)
            self.numbers.appendleft(number)
            self._current_max = number
        else:
            self.numbers.appendleft(number)

    def get(self):
        res = self.numbers.popleft()
        if res == self._current_max:
            self.maxes.popleft()
            self._current_max = self.maxes.popleft()
            self.maxes.appendleft(self._current_max)

        return res

    def get_max(self):
        return self._current_max


if __name__ == '__main__':
    stm = StackWithMax()
    for i in [3, 1, 2, 3, 5, 6, 70, 70, 5, 49]:
        stm.put(i)

    for _ in range(9):
        print("---" * 14)
        print(stm.get_max())
        print(f"{stm.get()=}")
        print(stm.get_max())
