import socket
from request import Request
from response import Response
import time
from collections import defaultdict
from threading import Thread

code = 'utf-8'


def send_url():
    global sock
    urls = ['https://mail.ru', 'https://mephi.ru', 'https://stackoverflow.com']
    json_data = Request.create(method='GET', text=urls)
    while True:
        try:
            sock.send(json_data.encode(code))
        except socket.timeout:
            print('send data timeout')
        except socket.error as ex:
            # print('send data error', ex)
            break
        time.sleep(2)
        

def get_result():
    global sock
    result=defaultdict(str)
    while True:
        try:
            json_data = sock.recv(1024)
            if not json_data:
                break
            response = Response(json_data.decode(code))
            if response.text:
                result[response.th]+=''.join(response.text)


        except socket.timeout:
            pass
        except socket.error as ex:
            print(result)
            # print('get data error', ex)
            break




if __name__ == '__main__':
    with socket.create_connection(('127.0.0.1', 10003), 10) as sock:
        sock.settimeout(10)

        th1 = Thread(target=send_url)
        th2 = Thread(target=get_result)

        th1.start()
        th2.start()

        th1.join()
        th2.join()




#
# import socket
# from request import Request
# import time
#
# from threading import Thread
#
# code = 'utf-8'
#
#
# def send_url():
#     global sock
#
#     urls = ['https://mail.ru', 'https://mephi.ru', 'https://stackoverflow.com']
#     while True:
#
#         sock.sendall(str(urls[count2:count2+4]).encode(code))
#         count2+=4
#         if count2>40:
#             break
#         print('отправили', count2)
#
#         time.sleep(1)
#         if count2>50:
#             time.sleep(30)
#
#
# def get_result():
#     global sock
#     global count
#     while True:
#         result = ''
#
#         data = sock.recv(1024)
#         print(data)
#         count += 1
#         print("получили",count)
#         if data:
#             result += data.decode(code)
#
#         if count>55:
#             break
#
#
#
#
# if __name__ == '__main__':
#
#     with socket.create_connection(('127.0.0.1', 10015), 10) as sock:
#         sock.settimeout(10)
#
#         th1 = Thread(target=send_url)
#         th2 = Thread(target=get_result)
#
#         th1.start()
#         th2.start()
#
#         th1.join()
#         th2.join()
#
