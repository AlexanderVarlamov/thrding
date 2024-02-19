"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 13.01.2024
@time 10:47
"""


def find_a_way(path: str):
    set_of_prev = {'0.0'}
    prev_point = [0, 0]
    for symb in path:
        if symb == 'u':
            next_point = [prev_point[0], prev_point[1] + 1]
        elif symb == 'd':
            next_point = [prev_point[0], prev_point[1] - 1]
        elif symb == 'l':
            next_point = [prev_point[0] - 1, prev_point[1]]
        elif symb == 'r':
            next_point = [prev_point[0] + 1, prev_point[1]]
        else:
            raise Exception('Неизвестный символ')

        point_to_set = '.'.join(map(str, next_point))
        if point_to_set in set_of_prev:
            print('yes')
            return
        else:
            set_of_prev.update([point_to_set])
            prev_point = next_point

    print('no')


paths = ['uurrdlll', 'uurrdldd']

for path in paths:
    find_a_way(path)
