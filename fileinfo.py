#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys,os
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import xlwt

def getfileinfo(info):
    filepath=info.split(',')[1]
    try:
        duration=re.findall(ur'(?<=Duration: ).+?(?=,)',info)[0]
    except:
        duration=""
    try:
        bitrate=int(re.findall(ur'(?<=bitrate: ).+?(?=kb/s)',info)[0])
    except:
        bitrate=0
    try:
        width=re.findall(ur'[1-9]\d+x+[1-9]\d+?(?= |,)',info)[0]
    except:
        width=""
    print width
    return [filepath,duration,bitrate,width]
def excel_insert(sheet,moviedata,row):
    for col in range(0,len(moviedata)):
        sheet.write(row,col,u'%s'%moviedata[col])
if __name__=='__main__':
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["路径","时长","码率","分辨率"],0)
    file = open("fileinfo.txt")
    row=1
    for line in file:
        movie = getfileinfo(line)
        if movie:
            excel_insert(sheet,movie,row)
        else:
            excel_insert(sheet,[line],row)
        row=row+1
        workbook.save("fileinfo.xls")