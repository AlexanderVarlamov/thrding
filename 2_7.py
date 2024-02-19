"""
version 
@author varlamov.a
@email varlamov.a@rt.ru
@date 15.01.2024
@time 16:39
"""

import threading

stor_local = threading.local()


def print_msg():
    msg = stor_local.msg if hasattr(stor_local, 'msg') else 'failure'
    fileno = stor_local.fileno if hasattr(stor_local, 'fileno') else 'failure'
    permission = stor_local.permission if hasattr(stor_local, 'permission') else 'guest'
    print(f"{msg}, fileno={fileno}, {permission}")

print_msg()