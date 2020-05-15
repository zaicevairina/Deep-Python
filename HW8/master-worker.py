# import socket
# import re
# import requests
# from request import Request
# from response import Response
# from bs4 import BeautifulSoup
# from queue import Queue
# from threading import Thread
#
# code = 'utf-8'
#
# def worker(q,i):
#     global conn
#     global c
#     global c2
#     while True:
#         url = q.get()
#         if url is None:
#             break
#         else:
#             c2+=1
#             print('gполчили ',c2)
#             # try:
#             #     # html = requests.get(url)
#             #     pass
#             # except ConnectionError:
#             #     json_answer = Response.create(code=500, error='No connection')
#             #     conn.send(json_answer.encode(code))
#             #
#             # if html.status_code != 200:
#             #     json_answer = Response.create(code=html.status_code, error='Can not get info')
#             #     conn.send(json_answer.encode(code))
#             # bs = BeautifulSoup(html.text, 'html.parser')
#             # answer = bs.get_text()
#             # print(f'Thread #{i} complites {url}')
#             c += 1
#             print("вернули ",c)
#             x = f' Thread #{i} complites {url}'
#
#             # conn.sendall(x.encode(code))
#             # conn.sendall(answer.encode(code))
#
#
#
# if __name__ == "__main__":
#     n_worker = input()
#     if not n_worker.isnumeric():
#         print('it is not number, try again')
#         n_worker = input()
#     n_worker=int(n_worker)
#
#     q = Queue(100)
#     ths = [Thread(target=worker, args=(q, i)) for i in range(n_worker)]
#
#     for th in ths:
#         th.start()
#
#     with socket.socket() as sock:
#         c=0
#         c2=0
#         sock.bind(('127.0.0.1', 10015))
#         sock.listen(0)
#
#         while True:
#             conn, addr = sock.accept()
#             conn.settimeout(10)
#             with conn:
#                 while True:
#                     try:
#                         json_data = conn.recv(1024)
#                     except socket.timeout:
#                         print('close connection by timeout')
#                         break
#                     if not json_data:
#                         break
#
#                     request = Request(json_data.decode(code))
#
#                     if not request.url:
#                         json_answer = Response.create(code=400, error='Bad request')
#                         conn.send(json_answer.encode(code))
#
#                     elif request.method != 'GET':
#                         json_answer = Response.create(code=405, error='Invalid method')
#                         conn.send(json_answer.encode(code))
#
#                     else:
#                         urls = request.url
#                         print(urls)
#                         for url in urls:
#                             q.put(url)
#                     del request
#
#
#     for _ in range(ths):
#         q.put(None)
#
#     for th in ths:
#         th.join()
#
#
#


import socket
import re
import requests
from request import Request
from response import Response
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread, RLock
import signal
import os
from time import sleep

code = 'utf-8'
def signal_f(signum, frame):
    global count
    global conn
    with q.mutex:
        q.queue.clear()
    for _ in range(len(ths)):
        q.put(None)

    for th in ths:
        th.join()
    print('Number of urls - ',count)
    if conn:
        conn.close()

def worker(q,i):
    global conn
    global count
    global mutex
    while True:
        url = q.get()
        if url is None:
            break
        else:
            html = requests.get(url)
            bs = BeautifulSoup(html.text, 'html.parser')
            answer = bs.get_text()
            json_data = Response.create(code='200', text=f'*****{url}*****',th=i)
            conn.sendall(json_data.encode(code))
            for j in range(0,len(answer),30):
                json_data = Response.create(code='200', text=answer[j:j+30],th=i)
                conn.send(json_data.encode(code))
                sleep(0.05)
            with mutex:
                count+=1
            print( f' Thread #{i} complites {url}')
        




if __name__ == "__main__":
    count=0
    mutex = RLock()
    print(f'pid={os.getpid()}')
    print('Введите число процессов')
    n_worker = input()
    if not n_worker.isnumeric():
        print('it is not number, try again')
        n_worker = input()
    n_worker = int(n_worker)

    q = Queue(100)
    ths = [Thread(target=worker, args=(q, i+1)) for i in range(n_worker)]
    signal.signal(signal.SIGUSR1, signal_f)

    for th in ths:
        th.start()

    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 10003))
        sock.listen(0)
        while True:
            conn, addr = sock.accept()
            conn.settimeout(100)
            with conn:

                while True:
                    try:
                        json_data = conn.recv(1024)
                        if not json_data:
                            break
                        request = Request(json_data.decode(code))
                        urls = request.text
                        for url in urls:
                            q.put(url)
                    except OSError:
                        break
            break




