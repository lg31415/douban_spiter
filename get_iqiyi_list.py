#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import urllib
import json
import sys
import re
import xlwt
import traceback
LIST_URL='http://media.skyworthbox.com/videoApi/api2.0/videolist.action?'
def get_chnId(chnid,tagId,pn):
    url = LIST_URL + 'chnId='+str(chnid)+'&tagId='+str(tagId)+'&pn='+str(pn)+'&ps=1000'
    print url
    headers = {'channel': 'qmz',
           'token': '15060920449364yGz%2BJa6diV1o%2BTYa6kcYA%3D%3D%0A_89201951'}
    r = requests.post(url, headers=headers)
    if r.status_code != 200:
        return
    data = r.text.encode('utf-8')
    items = json.loads(data)['data']
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["类型","名称","集数","年代","图片","时长","评分","描述"],0)
    row=0
    for i in items:
        # print [chnid,i['name'],i['seriesText'],i['issueTime'],i['picUrl'],i['timeLength'],i['doubanScore'],i['summary']]
        try:
            excel_insert(sheet,[chnid,i['name'],i['seriesText'],i['issueTime'],i['picUrl'],i['timeLength'],i['doubanScore'],i['summary']],row)
        except:
            return
        row+=1
        workbook.save(str(chnid)+"_"+str(tagId)+"_"+str(pn)+"_"+"all.xls")
def excel_insert(sheet,moviedata,row):
    # 获取MYSQL里面的数据字段名称
    # 获取并写入数据段信息
    for col in range(0,len(moviedata)):
        sheet.write(row,col,u'%s'%moviedata[col])
for a in range(0,5):
    for b in range(0,2):
        for c in range(0,10):
            get_chnId(a,b,c)
# if __name__=='__main__':
#     workbook = xlwt.Workbook()
#     sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
#     excel_insert(sheet,["关键字","名称","分数","年份","导演","演员","类型","集数","语言","发行年"," 时长","地区","图片","描述"],0)
#     file = open("241")
#     row=1
#     for line in file:
#         movie = search_douban(line)
#         if movie:
#             excel_insert(sheet,parse(movie),row)
#         else:
#             excel_insert(sheet,[line],row)
#         row=row+1
#         workbook.save("1671.xls")