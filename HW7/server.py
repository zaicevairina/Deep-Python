import socket
import re
import requests
from request import Request
from response import Response
from bs4 import BeautifulSoup

from nltk.corpus import stopwords

stops = set(stopwords.words('russian')).union(set(stopwords.words('english')))
code = 'cp1251'
regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

with socket.socket() as sock:
    sock.bind(('127.0.0.1', 10002))
    sock.listen(0)

    while True:
        conn, addr = sock.accept()
        conn.settimeout(10)
        with conn:
            while True:
                try:
                    json_data = conn.recv(1024)
                except socket.timeout:
                    print('close connection by timeout')
                    break
                if not json_data:
                    break

                request = Request(json_data.decode(code))

                if not request.url:
                    json_answer = Response.create(code=400, error='Bad request')
                    conn.send(json_answer.encode(code))

                elif request.method != 'GET':
                    json_answer = Response.create(code=405, error='Invalid method')
                    conn.send(json_answer.encode(code))

                elif not re.match(regex, request.url):
                    json_answer = Response.create(code=400, error='Bad request')
                    conn.send(json_answer.encode(code))

                else:
                    try:
                        html = requests.get(request.url)

                    except ConnectionError:
                        json_answer = Response.create(code=500, error='No connection')
                        conn.send(json_answer.encode(code))

                    if html.status_code != 200:
                        json_answer = Response.create(code=html.status_code, error='Can not get info')
                        conn.send(json_answer.encode(code))

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
                        if len(answer) < 10 and not (pair[0] in stops or len(pair[0]) == 1 or pair[0].isnumeric()):
                            answer.append(pair)
                        elif len(answer) == 10:
                            break

                    json_answer = Response.create(code=html.status_code, answer=answer)
                    conn.sendall(json_answer.encode(code))
