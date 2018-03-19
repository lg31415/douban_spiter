#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import multiprocessing
import requests
import lxml.html
import time
from bs4 import BeautifulSoup
import xlwt
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

def getPiaofang(title):
    #根据电影名字形成猫眼上该电影的搜索结果页面
    url = 'http://pf.maoyan.com/search?key='+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    decurl="http://pf.maoyan.com"+soup.find(attrs={'class':'indentInner canTouch'})['data-url']
    decr = requests.get(decurl,headers=headers)
    decsoup = BeautifulSoup(decr.text.encode('utf-8'), 'lxml')
    return  decsoup.find(attrs={'class':'wish-val'}).text.replace('\n','').replace(' ','')
    # print soup
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
def getTencentAll(title):
    url = 'https://v.qq.com/x/search/?q='+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    decurl= soup.find_all('a', attrs={'class': "figure result_figure"})[0]['href']
    decr = requests.get(decurl,headers=headers)
    decsoup = BeautifulSoup(decr.text.encode('utf-8'), 'lxml')
    playurl= decsoup.find_all('a', attrs={'class':"btn_primary btn_primary_md "})[0]['href']
    decr1 = requests.get(playurl,headers=headers)
    dec1soup = BeautifulSoup(decr1.text.encode('utf-8'), 'lxml')
    return dec1soup.find(attrs={'id':'mod_cover_playnum'}).text.encode('utf-8')
def getMgtv(title):
    url = 'https://v.qq.com/x/search/?q='+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    decurl= soup.find_all('a', attrs={'class': "figure result_figure"})[0]['href']
    decr1 = requests.get(decurl,headers=headers)
    dec1soup = BeautifulSoup(decr1.text.encode('utf-8'), 'lxml')
    dec1url= dec1soup.find_all('a', attrs={'class': "btn_primary btn_primary_md "})[0]['href']
    decr2 = requests.get(dec1url,headers=headers)
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
    driver.get(dec1url)
    data = driver.page_source
    dec2soup = BeautifulSoup(data.encode('utf-8'), 'lxml')
    # print dec2soup
    # print dec2soup.find(attrs={'id':'honey-click-stats'})
    return dec2soup.find(attrs={'id':'honey-click-stats'}).text.encode('utf-8')

def getAiqiyi(title):
    url = 'http://so.iqiyi.com/so/q_'+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    try:
        decurl= soup.find_all('a', attrs={'class': "album_link"})[0]['href'].replace('www.iqiyi','m.iqiyi')
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/537.4 Maxthon/%s')  #根据需要设置具体的浏览器信息
        driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
        driver.get(decurl)
        data = driver.page_source
        decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
        result=decsoup.find(attrs={'glue-bind':'count'}).text
    except:
        decurl= soup.find_all('a', attrs={'class': "info_play_btn"})[0]['href'].replace('www.iqiyi','m.iqiyi')
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/537.4 Maxthon/%s')  #根据需要设置具体的浏览器信息
        driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
        driver.get(decurl)
        data = driver.page_source
        decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
        result=decsoup.find(attrs={'class':'c-data-num'}).text
    driver.close()
    return result
def getAiqiyiAll(title):
    url = 'http://so.iqiyi.com/so/q_'+title
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    try:
        decurl= soup.find_all('a', attrs={'class': "info_play_btn"})[0]['href'].replace('www.iqiyi','m.iqiyi')
    except:
        decurl= soup.find_all('a', attrs={'data-widget-qidanadd': "qidanadd"})[0]['href'].replace('www.iqiyi','m.iqiyi')
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/537.4 Maxthon/%s')  #根据需要设置具体的浏览器信息
    driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
    driver.get(decurl)
    data = driver.page_source
    decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
    playurl=decsoup.find_all('a', attrs={'id': "album_title_a"})[0]['href']
    driver.get(playurl)
    data = driver.page_source
    decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
    driver.close()
    return decsoup.find(attrs={'glue-bind':'count'}).text
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
        piaofang=getPiaofang(title)
    except:
        piaofang="未知"
    try:
        tencentnum=getTencent(title)
    except:
        try:
            tencentnum=getTencentAll(title)
        except:
            try:
                tencentnum=getMgtv(title)
            except:
                tencentnum="未知"
    try:
        aiqiyinum=getAiqiyi(title)
    except:
        try:
            aiqiyinum=getAiqiyiAll(title)
        except:
            aiqiyinum="未知"
    try:
        youkunum=getYouku(title)
    except:
        youkunum="未知"
    return [title,"",piaofang,"",tencentnum,aiqiyinum,youkunum]


def convert(file1,file2):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["名称","类型","票房","出品方","腾讯网络累计播放量","爱奇艺网络累计播放量","优酷网络累计播放量"],0)
    # excel_insert(sheet,["名称","票房"],0)
    file = open(file1)
    row=1
    for line in file:
        movie = moveinfo(line)
        if movie:
            excel_insert(sheet,movie,row)
        else:
            excel_insert(sheet,[line],row)
        row=row+1
        time.sleep(3)
        workbook.save(file2)
# if __name__=='__main__':
#     input = sys.argv[1]
#     output = sys.argv[2]
#     # record = []
#     # for i in range(8):
#     #     process = multiprocessing.Process(target=convert,args=(input,output))
#     #     process.start()
#     #     record.append(process)
#     # for process in record:
#     #     process.join()
#
#     input = sys.argv[1]
#     output = sys.argv[2]
#     convert(input,output)
print getAiqiyi("天生是优我")
