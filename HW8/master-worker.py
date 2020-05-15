

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




