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
import time
import re
import xlwt
import traceback
from baidu_spider import search_baidu

SEARCH_URL='http://www.soku.com/search_video/q_'
SEARCH_URL_API='http://api.douban.com/v2/movie/search?q='
PAGE_URL='https://movie.douban.com/subject/%s/'
class Movie(object):
    def __init__(self):
        self.id = ''
        self.text = ''
        self.title = ''
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
        self.showid = ''


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
def search_youku(text):
    url = SEARCH_URL +text
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    movie=Movie()
    # movie.imgurl=soup.find(attrs={'class':'poster-link'}).get('href')
    movie.text=text.encode('utf-8')
    try:
        movie.type=soup.find(attrs={'class':'base_type'}).text
    except:
        movie.type=""
    try:
        movie.director=soup.find(attrs={'class':'s_direct'}).text.replace('导演：','')
    except:
        movie.director=""
    try:
        movie.actor=soup.find(attrs={'class':'s_figure'}).text.replace('主演：','')
    except:
        movie.actor=""
    try:
        movie.area=soup.find(attrs={'class':'s_area'}).text
    except:
        movie.area=""
    try:
        movie.dec=soup.find(attrs={'class':'info_cont'}).text
    except:
        movie.dec=""
    try:
        movie.showid= soup.find(attrs={'class':'info_cont'}).a['_iku_showid']
    except:
        movie.showid=""
    # print movie.imgurl
    # search_baidu(text)
    return [movie.text,movie.type,movie.director,movie.actor,movie.area,movie.dec,movie.showid]+search_baidu(text)
def get_movie_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    movie=Movie()

def excel_insert(sheet,moviedata,row):
    for col in range(0,len(moviedata)):
       sheet.write(row,col,u'%s'%moviedata[col])

if __name__=='__main__':
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["名称","类型","导演","演员","地区","描述","YouKuShowID"],0)
    file = open("241")
    row=1
    for line in file:
        movie = search_youku(line)
        if movie:
            excel_insert(sheet,movie,row)
        else:
            excel_insert(sheet,[line],row)
        row=row+1
        time.sleep(3)
        workbook.save("42_youku.xls")