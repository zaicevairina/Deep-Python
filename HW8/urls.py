import socket
from request import Request
from response import Response
import time
from queue import Queue

code = 'utf-8'
from threading import Thread, RLock


def send_url(q, i):
    global sock
    global mutex
    while True:
        url = q.get()
        if url is None:
            break
        json_data = Request.create(method='GET', text=url)
        try:
            with mutex:
                # print(time.time(),'send i   ',json_data)
                sock.send(json_data.encode(code))
        except socket.timeout:
            print('send data timeout')
        except socket.error as ex:
            # print('send data error', ex)
            break


def get_result(count):
    global sock
    k = 0
    while True:
        try:
            json_data = sock.recv(1024)
            if not json_data:
                break
            response = Response(json_data.decode(code))
            if response.text:
                print(k, ' ,', response.text)
                k += 1
            if count == k:
                print('Finish')
                break
        except socket.timeout:
            break
        except socket.error as ex:
            # print('get data error', ex)
            break


if __name__ == '__main__':
    print('Введите файл')
    file=input()
    try:
        with open(file) as f:
            file = f.read()
            urls = file.split('\n')
    except:
        print('Ошибка, введите еще раз')
        input()
    print('Введите число потоков')
    m = input()
    if not m.isnumeric():
        print('it is not number, try again')
        m = input()
    m = int(m)

    mutex = RLock()
    with socket.create_connection(('127.0.0.1', 10006), 10) as sock:
        sock.settimeout(15)
        th_listen = Thread(target=get_result, args=(len(urls),))
        q = Queue(len(urls))
        ths = [Thread(target=send_url, args=(q, i + 1)) for i in range(m)]
        for th in ths:
            th.start()
        th_listen.start()
        for url in urls:
            q.put(url)
            time.sleep(1)
        for i in range(m):
            q.put(None)
        for th in ths:
            th.join()
        th_listen.join()

