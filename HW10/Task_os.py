
import os
import time
import xlwt

def info_about_dir(path):
    path_d = path.count('\\')
    wb = xlwt.Workbook()
    ws = wb.add_sheet('info_about_dir',cell_overwrite_ok=True)
    num = 0

    for i,k in enumerate(os.walk(path)):
        for filename in k[2]:
            row = ws.row(num)
            num+=1
            abs_path=os.path.abspath(k[0])+'\\'+filename
            data = [filename,'file',os.path.getsize(abs_path),time.ctime(os.path.getmtime(abs_path)),k[0].count('\\')-path_d+1,abs_path]
            for index in range(len(data)):
                row.write(index,data[index])
        for dirname in k[1]:
            row = ws.row(num)
            num += 1
            abs_path = os.path.abspath(k[0]) + '\\' + dirname
            data=[dirname,'dir',os.path.getsize(abs_path),time.ctime(os.path.getmtime(abs_path)),k[0].count('\\')-path_d+1,abs_path]
            for index in range(len(data)):
                row.write(index,data[index])
    wb.save('info_about_dir.xls')

info_about_dir(path=r'C:\Users\Ирина\PycharmProjects\Deep-Python\HW10\test')