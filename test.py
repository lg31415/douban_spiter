#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import lxml.html
import time
from bs4 import BeautifulSoup
import xlwt

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

def getPiaofang(title):
    #根据电影名字形成猫眼上该电影的搜索结果页面
    url = 'http://pf.maoyan.com/search?key='+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    # print soup
    return soup.find(attrs={'class':'cs'}).text
def getCbooo(title):
    #根据电影名字形成猫眼上该电影的搜索结果页面
    url = 'http://www.cbooo.cn/search?k='+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    # print soup
    decurl= soup.find_all('a', attrs={'target':"_blank"})[1]['href']
    decr = requests.get(decurl,headers=headers)
    decsoup = BeautifulSoup(decr.text.encode('utf-8'), 'lxml')
    return  decsoup.find(attrs={'class':'tit-xq'}).text.replace('\n','').replace(' ','')
def getTencent(title):
    url = 'https://v.qq.com/x/search/?q='+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    decurl= soup.find_all('a', attrs={'class': "figure result_figure"})[0]['href']
    decr = requests.get(decurl,headers=headers)
    decsoup = BeautifulSoup(decr.text.encode('utf-8'), 'lxml')
    return decsoup.find(attrs={'id':'mod_cover_playnum'}).text.encode('utf-8')
def getAiqiyi(title):
    url = 'http://so.iqiyi.com/so/q_'+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    decurl= soup.find_all('a', attrs={'class': "info_play_btn"})[0]['href']
    decr = requests.get(decurl,headers=headers)
    decsoup = BeautifulSoup(decr.text.encode('utf-8'), 'lxml')
    return decsoup.find(attrs={'data-chart-elem':'playNum'}).text
def getYouku(title):
    url = 'http://www.soku.com/search_video/q_'+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    return  soup.find(attrs={'class':'num'}).text
def excel_insert(sheet,moviedata,row):
    for col in range(0,len(moviedata)):
       sheet.write(row,col,u'%s'%moviedata[col])
def moveinfo(title):
    try:
        piaofang=getCbooo(title)
    except:
        piaofang="未知"
    try:
        tencentnum=getTencent(title)
    except:
        tencentnum="未知"
    try:
        aiqiyinum=getAiqiyi(title)
    except:
        aiqiyinum="未知"
    try:
        youkunum=getYouku(title)
    except:
        youkunum="未知"
    return [title,'',piaofang,"",tencentnum,aiqiyinum,youkunum]

if __name__=='__main__':
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["名称","类型","票房","出品方","腾讯网络累计播放量","爱奇艺网络累计播放量","优酷网络累计播放量"],0)
    file = open("242")
    row=1
    for line in file:
        movie = moveinfo(line)
        if movie:
            excel_insert(sheet,movie,row)
        else:
            excel_insert(sheet,[line],row)
        row=row+1
        time.sleep(3)
        workbook.save("hubeiplaynum.xls")