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
SEARCH_URL="http://search.pptv.com/result?search_query="
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
def search_pptv(text,type):
    url=SEARCH_URL+text+"&result_type="+str(type)
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    movie=Movie()
    movie.text=text.encode('utf-8')
    dec_url=soup.find(attrs={'class':'detailbtn'}).get('href')
    dec = requests.get(dec_url)
    dec_soup = BeautifulSoup(dec.text.encode('utf-8'), 'lxml')
    movie.epi= dec_soup.find(attrs={'class':'ba_jj'}).text
    string=dec_soup.find(attrs={'class':'infolist nocover cf'}).text.strip().replace("\n", "").encode('utf-8')
    movie.area=re.findall("主演：(.*?)：",string,re.DOTALL)[0][:-6]
    movie.director= re.findall("导演：(.*?)：",string,re.DOTALL)[0][:-6]
    movie.area= re.findall("地区：(.*?)：",string,re.DOTALL)[0][:-6]
    movie.type= re.findall("上映：(.*?)：",string,re.DOTALL)[0][:-6]
    movie.length= re.findall("片长：(.*?)：",string,re.DOTALL)[0][:-6].split(" ")[0]

if __name__ =='__main__':
    search_pptv("英雄",2)



