import socket
import re
from request import Request
from response import Response

code = 'cp1251'
regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


result = ''

url = input()

validate = (re.match(regex, url))
while True and not validate:
    print('Try plz again')
    url = input()
    validate = (re.match(regex, url))

with socket.create_connection(('127.0.0.1', 10002), 10) as sock:
    sock.settimeout(10)
    try:
        json_data = Request.create(method='GET', url=url)
        sock.sendall(json_data.encode(code))
    except socket.timeout:
        print('send data timeout')
    except socket.error as ex:
        print('send data error', ex)

    while True:
        try:
            data = sock.recv(1024)
            if data:
                result += data.decode(code)
        except socket.timeout:
            # print('get data timeout')
            break
        except socket.error as ex:
            print('get data error', ex)
            break
if result:
    response = Response(result)
    if response.code != 200:
        print(response.error)
    else:
        print(f'\n \n \n******* Top {len(response.answer)} words of the site {url}*******')
        for pair in response.answer:
            print(pair[0], pair[1])
