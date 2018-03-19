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
import urllib
import urllib2
import requests
import os
from bs4 import BeautifulSoup
import xlwt
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}


def getPageNum(shopname):
    url = "https://"+shopname+".tmall.com/category.htm"
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = ( 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  #根据需要设置具体的浏览器信息
    driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
    driver.get(url)
    data = driver.page_source
    # print data
    decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
    try:
        ItemNum=int(decsoup.find_all(attrs={'class':'ui-page-s'})[0].find_all(attrs={'class':'ui-page-s-len'})[0].text.split("/")[1])
    except:
        ItemNum=1
    return ItemNum
    # driver.get(playurl)
    # data = driver.page_source
    # decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
    # driver.close()
    # return decsoup.find(attrs={'glue-bind':'count'}).text
def getItemList(url):
    print url
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap['phantomjs.page.settings.userAgent'] = ( 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')  #根据需要设置具体的浏览器信息
    driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
    driver.get(url)
    data = driver.page_source
    decsoup = BeautifulSoup(data.encode('utf-8'), 'lxml')
    print decsoup
    ItemList=decsoup.find_all(attrs={'class':'item '})
    ItemListLast=decsoup.find_all(attrs={'class':'item last'})
    return ItemList+ItemListLast
    # print ItemList1
def getItemInfo(info):
    infoData=BeautifulSoup(info.encode('utf-8'), 'lxml')
    # print infoData.find(attrs={'class':'sale-num'}).text
    # print infoData.find(attrs={'class':'item-name J_TGoldData'}).text
    # print infoData.find(attrs={'class':'title'}).text
    # print infoData.find(attrs={'class':'c-price'}).text
    # print infoData.find(attrs={'class':'J_TGoldData'}).find('img')['data-ks-lazyload']
    # print "http:"+infoData.find(attrs={'class':'J_TGoldData'})['href']
    # print infoData.find(attrs={'class':'J_TGoldData'}).find('img')['alt'].replace(' ', '-')+".png"
    return [infoData.find(attrs={'class':'item-name J_TGoldData'}).text,infoData.find(attrs={'class':'sale-num'}).text,infoData.find(attrs={'class':'title'}).text,infoData.find(attrs={'class':'c-price'}).text,'http:'+infoData.find(attrs={'class':'J_TGoldData'}).find('img')['data-ks-lazyload'],"http:"+infoData.find(attrs={'class':'J_TGoldData'})['href'],infoData.find(attrs={'class':'J_TGoldData'}).find('img')['alt'].replace(' ', '-')+".png"]
# print getItemInfo(getItemList("https://hasbro.tmall.com/category.htm?pageNo=1")[1])
def excel_insert(sheet,moviedata,row):
    # 获取MYSQL里面的数据字段名称
    # 获取并写入数据段信息
    for col in range(0,len(moviedata)):
        sheet.write(row,col,u'%s'%moviedata[col])


def convert(file1,file2):
    # os.mkdir('imgdir')
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["店铺地址","宝贝名称","总销量","评价数","价格","图片地址","宝贝链接","图片文件"],0)
    nameList = open(file1)
    row=1
    for name in nameList:
        print name
        try:
            PageNumRange=getPageNum(name)
        finally:
            PageNumRange=1
        print PageNumRange
        try:
            for pageNum in range(1,PageNumRange+1):
                print pageNum
                for info in getItemList("https://hasbro.tmall.com/category.htm?pageNo="+str(pageNum)):
                    print info
                    item=['http://'+name+".tmall.com",]+getItemInfo(info)
                    print item
                    print item[5]
                    print 'imgdir\\'+item[7]
                    urllib.urlretrieve(item[5],'imgdir\\'+item[7])
                    if item:
                        excel_insert(sheet,item,row)
                    else:
                        excel_insert(sheet,[name],row)
                    row=row+1
            workbook.save(file2)
        finally:
            workbook.save(file2)
if __name__ =='__main__':
    convert("242","1.xls")