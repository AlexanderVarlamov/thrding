"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 18.01.2024
@time 17:37
"""

def get_card_number():
    for i in range(801):
        yield str(4007000000100 + i)


def do_request(card_number: str):
    print(card_number)

import concurrent.futures


with concurrent.futures.ThreadPoolExecutor(15) as executor:
    [executor.submit(do_request, card) for card in get_card_number()]