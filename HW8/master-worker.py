

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
import re

from nltk.corpus import stopwords

stops = set(stopwords.words('russian')).union(set(stopwords.words('english')))

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

def worker(q,i,top_N):
    global conn
    global count
    global mutex
    while True:
        url = q.get()
        if url is None:
            break
        else:
            try:
                html = requests.get(url)
                bs = BeautifulSoup(html.text, 'html.parser')
                answer = bs.get_text()
                answer = answer.replace('\n', ' ')
                answer = answer.replace('\t', ' ')
                answer = re.sub("[^а-яА-Я]", " ", answer)
                words = answer.split()
                dictionary = {}
                for word in words:
                    if word in dictionary:
                        dictionary[word] += 1
                    else:
                        dictionary[word] = 1
                list_d = list(dictionary.items())
                list_d.sort(key=lambda i: i[1], reverse=True)
                answer = []
                for pair in list_d:
                    if len(answer) < top_N and not (pair[0] in stops or len(pair[0]) == 1 or pair[0].isnumeric()):
                        answer.append(pair)
                    elif len(answer) == top_N:
                        break
                temp=''
                for pair in answer:
                    temp+=pair[0]+' '
                json_answer = Response.create(code=html.status_code, text=temp)
                # json_answer = Response.create(code=html.status_code, text=f' Thread #{i} complites {url}')

                conn.sendall(json_answer.encode(code))
                with mutex:
                    count+=1
                print( f' Thread #{i} complites {url}')
            except:
                json_answer = Response.create(code=html.status_code, text='error')
                conn.sendall(json_answer.encode(code))

        




if __name__ == "__main__":
    count=0
    mutex = RLock()
    print(f'pid={os.getpid()}')
    print('Введите число потоков')
    n_worker = input()
    if not n_worker.isnumeric():
        print('it is not number, try again')
        n_worker = input()
    n_worker = int(n_worker)

    print('Введите числ TOP N')
    top_N = input()
    if not top_N.isnumeric():
        print('it is not number, try again')
        top_N = input()
    top_N = int(top_N)

    q = Queue(100)
    ths = [Thread(target=worker, args=(q, i+1,top_N)) for i in range(n_worker)]
    signal.signal(signal.SIGUSR1, signal_f)

    for th in ths:
        th.start()

    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 10006))
        sock.listen(0)
        while True:
            conn, addr = sock.accept()
            conn.settimeout(5)
            with conn:
                while True:
                    try:
                        json_data = conn.recv(1024)
                        if not json_data:
                            break
                        request = Request(json_data.decode(code))
                        url = request.text
                        q.put(url)
                    except socket.timeout:
                        break
                    except OSError:
                        break
            break




