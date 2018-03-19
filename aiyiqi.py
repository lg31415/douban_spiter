#! /usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import requests
import urllib,os
SEARCH_URL='http://so.iqiyi.com/so/q_'
def search_aiqiyi(text):
    text = urllib.quote(text)
    url = SEARCH_URL + text
    r = requests.get(url)
    if r.status_code != 200:
        return
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    # print soup.find_all('a', attrs={'class':"result_album clearfix"})[0]
    decurl=soup.find_all('a', attrs={'data-playsrc-elem': "details"})[0]['href']
    decr = requests.get(decurl)
    if r.status_code != 200:
        return
    decsoup = BeautifulSoup(decr.text.encode('utf-8'), 'lxml')

    try:
        result=[soup.find_all('a', attrs={'class': "info_play_btn"})[0]['href'],]
    except:
        result= list(set([i.find('a')['href'] for i in soup.find_all('li', attrs={'class': "album_item"})]))
        # soup.find_all('li', attrs={'class': "album_item"})[1].find('a')['href']
    return  result

def excel_insert(sheet,moviedata,row):
    # 获取MYSQL里面的数据字段名称
    # 获取并写入数据段信息
    for col in range(0,len(moviedata)):
        sheet.write(row,col,u'%s'%moviedata[col])
def getfile(text):
    for url in search_aiqiyi(text):
        os.system('/usr/bin/you-get '+ url + ' -o /data/pukkaupload/download')
# getfile("我的仨妈俩爸")
search_aiqiyi("我的仨妈俩爸")