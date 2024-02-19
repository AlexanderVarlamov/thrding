"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 07.02.2024
@time 16:07
"""
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection


def sender(conn: Connection) -> None:
    message = "Hello from sender!"
    number = 42
    float_number = 3.14159
    with conn:
        conn.send(message)
        conn.send(number)
        conn.send(float_number)
        conn.send(bytearray(message.encode() + number.to_bytes(length=4, byteorder='big')))
        # отправьте number
        # отправьте float_number
        # отправьте bytearray


if __name__ == "__main__":
    recv_conn, send_conn = Pipe(duplex=False)
    Process(target=sender, args=[send_conn]).start()
    recv_data = []
    while recv_conn.poll(timeout=0.1):
        recv_data.append(recv_conn.recv())
    # получите данные и сформируйте recv_data
    print(recv_data)
