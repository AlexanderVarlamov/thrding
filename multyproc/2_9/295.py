"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 14.02.2024
@time 9:47
"""
from concurrent.futures import ProcessPoolExecutor

def crypto_utils(text: str) -> tuple[str, float]:
    if text.startswith("a"):
        return "aaa45678", 3.14159
    if text.startswith("b"):
        return "bbb45678", 2.777
    return "12345678", 1.001


text_blocks = ("allocation", "bombshell", "doom")

if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        processes = executor.map(crypto_utils, text_blocks)
    results = {}

    for proc, text in zip(processes, text_blocks):
        result = proc[0]
        quality = proc[1]
        results.update({result: (text, quality)})

    print(results)