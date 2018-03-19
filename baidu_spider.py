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

SEARCH_URL='http://v.baidu.com/v?ie=utf-8&word='
class Movie(object):
    def __init__(self):
        self.id = ''
        self.title = ''
        self.text = ''
        self.score = 0
        self.director = ''
        self.actor = ''
        self.year = ''
        self.type = ''
        self.language = ''
        self.length = ''
        self.area = ''
        self.epi = ''
        self.dec = ''
        self.imgurl = ''

    def __str__(self):
        text =  '===============   Douban Movie   ===============\n'+\
                '名称: ' + self.title + '\n' +\
                '评分: ' + str(self.score) + '\n' +\
                '年代: ' + self.year + '\n' +\
                '集数: ' + self.epi + '\n' +\
                '导演: ' + self.director + '\n' +\
                '演员: ' + self.actor + '\n' +\
                '类型: ' + self.type + '\n' +\
                '语言: ' + self.language + '\n' +\
                '上映日期: ' + self.year + '\n' +\
                '片长: ' + self.length + '\n' +\
                '地区: ' + self.area + '\n' +\
                '图片: ' + self.imgurl + '\n' +\
                '描述: ' + self.dec + '\n' +\
                '================================================'
        return text.encode('utf-8')
        # return [self.title,str(self.score),self.year,self.director,self.actor,self.type,self.language,self.years,self.length,self.area,self.imgurl,self.dec]
def search_baidu(text):
    url = SEARCH_URL + text
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    # print soup
    movie=Movie()
    # movie.imgurl=soup.find(attrs={'class':'poster-link'}).get('href')
    movie.text=text.encode('utf-8')
    try:
        movie.title= soup.find(attrs={'class':'poster-link'}).get('title')
    except:
        movie.title=text.encode('UTF-8')
    try:
        movie.language= re.findall("(.*?)\(",soup.find(attrs={'class':'info-wrap'}).text.encode('utf-8'),re.DOTALL)[0][-8:].encode('UTF-8')
    except:
        movie.language="普通话"
    try:
        movie.year= re.findall("\((.*?)\)",soup.find(attrs={'class':'info-wrap'}).text.encode('utf-8'),re.DOTALL)[0]
    except:
        movie.year=""
    try:
        movie.score= soup.find(attrs={'class':'newest'}).text
    except:
        movie.score=""
    try:
        movie.imgurl=soup.find(attrs={'alt':soup.find(attrs={'class':'poster-link'}).get('title')}).get('src')
    except:
        movie.imgurl=""
    print movie.imgurl
    try:
        movie.epi=soup.find(attrs={'class':'update-info'}).text
    except:
        movie.epi="1"
    try:
        string=soup.find(attrs={'class':'intro-items'}).text.strip().replace("\n", "").encode('utf-8')
    except:
        string=""
    try:
        movie.director= re.findall("导演：(.*?)：",string,re.DOTALL)[0][:-6]
    except:
        try:
            movie.director= re.findall("作者：(.*?)：",string,re.DOTALL)[0][:-6]
        except:
            movie.director='无'
    try:
        movie.actor= re.findall("主演：(.*?)：",string,re.DOTALL)[0][:-6]
    except:
        movie.actor='无'
    try:
        movie.type= re.findall("类型：(.*?)：",string,re.DOTALL)[0][:-6]
    except:
        movie.type='无'
    try:
        movie.area= re.findall("地区：(.*?)：",string,re.DOTALL)[0][:-6]
    except:
        movie.area='无'
    try:
        movie.dec= re.findall("简介：(.*?)查看详情",string,re.DOTALL)[0]
    except:
        movie.dec='无'
    print  movie.title
        # ,str(movie.score),movie.year,movie.director,movie.actor,movie.type,movie.epi,movie.language,movie.year,movie.length,movie.area,movie.imgurl,movie.dec
    return [movie.text,movie.title,str(movie.score),movie.year,movie.director,movie.actor,movie.type,movie.epi,movie.language,movie.year,movie.length,movie.area,movie.imgurl,movie.dec]
def excel_insert(sheet,moviedata,row):
    # 获取MYSQL里面的数据字段名称
    # 获取并写入数据段信息
    for col in range(0,len(moviedata)):
       sheet.write(row,col,u'%s'%moviedata[col])
if __name__=='__main__':
    search_baidu('神探夏洛克')


# if __name__=='__main__':
#     workbook = xlwt.Workbook()
#     sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
#     excel_insert(sheet,["关键字","名称","分数","年份","导演","演员","类型","集数","语言","发行年"," 时长","地区","图片","描述"],0)
#     file = open("241")
#     row=1
#     for line in file:
#         movie = search_baidu(line)
#         if movie:
#             excel_insert(sheet,movie,row)
#         else:
#             excel_insert(sheet,[line],row)
#         row=row+1
#         workbook.save("385.xls")

    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    # excel_insert(sheet,["名称","分数","年份","导演","演员","类型","集数","语言","发行年"," 时长","地区","图片","描述"],0)
    # file = open("ser.txt")
    # row=1
    # for line in file:
    #     movie = search_baidu(line)
    #     if movie:
    #         excel_insert(sheet,parse(movie),row)
    #     else:
    #         excel_insert(sheet,[line],row)
    #     row=row+1
    # workbook.save("ser.xls")

    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    # excel_insert(sheet,["名称","分数","年份","导演","演员","类型","集数","语言","发行年"," 时长","地区","图片","描述"],0)
    # file = open("dongman.txt")
    # row=1
    # for line in file:
    #     movie = search_baidu(line)
    #     if movie:
    #         excel_insert(sheet,parse(movie),row)
    #     else:
    #         excel_insert(sheet,[line],row)
    #     row=row+1
    # workbook.save("dongman.xls")



    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    # file = open("movie.txt")
    # row=1
    # for line in file:
    #     excel_insert(sheet,parse(search(line)),row)
    #     row=row+1
    # workbook.save("movie.xls")

