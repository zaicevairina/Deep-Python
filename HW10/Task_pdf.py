
filename='test.pdf'

with open(filename,'rb') as f:
    data = f.read()
    data=data.decode('ISO-8859-1')
    data=data[data.find('Count '):]
    print(data[6:data[data.find('Count '):].find('/')])

