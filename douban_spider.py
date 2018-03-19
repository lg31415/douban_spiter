#! /usr/bin/python
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

SEARCH_URL='https://movie.douban.com/j/subject_suggest?q='
SEARCH_URL_API='http://api.douban.com/v2/movie/search?q='
PAGE_URL='https://movie.douban.com/subject/%s/'
def single_get_first(unicode1):
    str1 = unicode1.decode('utf-8').encode('gbk')
    try:
        return chr(ord(str1))
    except:
        asc = ord(str1[0])*256 + ord(str1[1]) - 65536

    if asc >= -20319 and asc <= -20284:
        return 'a'
    if asc >= -20283 and asc <= -19776:
        return 'b'
    if asc >= -19775 and asc <= -19219:
        return 'c'
    if asc >= -19218 and asc <= -18711:
        return 'd'
    if asc >= -18710 and asc <= -18527:
        return 'e'
    if asc >= -18526 and asc <= -18240:
        return 'f'
    if asc >= -18239 and asc <= -17923:
        return 'g'
    if asc >= -17922 and asc <= -17418:
        return 'h'
    if asc >= -17417 and asc <= -16475:
        return 'j'
    if asc >= -16474 and asc <= -16213:
        return 'k'
    if asc >= -16212 and asc <= -15641:
        return 'l'
    if asc >= -15640 and asc <= -15166:
        return 'm'
    if asc >= -15165 and asc <= -14923:
        return 'n'
    if asc >= -14922 and asc <= -14915:
        return 'o'
    if asc >= -14914 and asc <= -14631:
        return 'p'
    if asc >= -14630 and asc <= -14150:
        return 'q'
    if asc >= -14149 and asc <= -14091:
        return 'r'
    if asc >= -14090 and asc <= -13119:
        return 's'
    if asc >= -13118 and asc <= -12839:
        return 't'
    if asc >= -12838 and asc <= -12557:
        return 'w'
    if asc >= -12556 and asc <= -11848:
        return 'x'
    if asc >= -11847 and asc <= -11056:
        return 'y'
    if asc >= -11055 and asc <= -10247:
        return 'z'
    return ''
def getPinyin(string):
    if string==None:
        return None
    lst = list(string)
    charLst = []
    for l in lst:
        charLst.append(single_get_first(l))
    return  ''.join(charLst)
def saveImg1(imgurl,imgpath,headers):
    response = requests.get(imgurl,headers=headers)
    with open(imgpath, 'wb') as f:
        f.write(response.content)
        f.flush()
class Movie(object):
    def __init__(self):
        self.id = ''
        self.text = ''
        self.title = ''
        self.score = 0
        self.director = ''
        self.actor = ''
        self.firstplay = ''
        self.type = ''
        self.language = ''
        self.length = ''
        self.area = ''
        self.epi = ''
        self.dec = ''
        self.imgurl = ''
        self.pinyin=''

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
                '上映日期: ' + self.firstplay + '\n' +\
                '片长: ' + self.length + '\n' +\
                '地区: ' + self.area + '\n' +\
                '图片: ' + self.imgurl + '\n' +\
                '描述: ' + self.dec + '\n' +\
                '================================================'
        return text.encode('utf-8')
        # return [self.title,str(self.score),self.year,self.director,self.actor,self.type,self.language,self.years,self.length,self.area,self.imgurl,self.dec]
def search_douban(text):
    text = urllib.quote(text)
    url = SEARCH_URL + text
    r = requests.get(url)
    if r.status_code != 200:
        return
    data = r.text.encode('utf-8')
    items = json.loads(data)
    if len(items) == 0:
        return
    movie = Movie()
    movie.text=text.encode('utf-8')
    movie.id = items[0]['id']
    movie.title = items[0]['title']
    movie.pinyin=getPinyin(movie.title)
    movie.year = items[0]['year']
    print movie.pinyin
    return movie

# def search_douban(text):
#     text = urllib.quote(text)
#     url = SEARCH_URL_API + text
#     r = requests.get(url)
#     if r.status_code != 200:
#         return
#
#     data = r.text.encode('utf-8')
#     items = json.loads(data)
#     if len(items) == 0:
#         return
#     movie = Movie()
#     try:
#         movie.id = items['subjects'][0]['id']
#         movie.title = items['subjects'][0]['title']
#         movie.year = items['subjects'][0]['year']
#     except:
#         movie.id = '26270502'
#         movie.title =text
#         movie.year ='未知'
#     return movie

def parse(movie):
    url = PAGE_URL % movie.id
    imgurl="https://movie.douban.com/subject/"+movie.id+"/photos?type=R"
    r = requests.get(url)
    soup = BeautifulSoup(r.text.encode('utf-8'), 'lxml')
    try:
        info = soup.select('#info')[0]
    except:
        info=""
    try:
        movie.area= re.findall(ur'(?<=制片国家/地区: ).+?(?=\n)', info.text)[0]
    except:
        movie.area="大陆"
    try:
        movie.language= re.findall(ur'(?<=语言: ).+?(?=\n)', info.text)[0]
    except:
        movie.length="未知"
    try:
        movie.firstplay= re.findall(ur'(?<=首播: ).+?(?=\n)', info.text)[0]
    except:
        movie.firstplay= re.findall(ur'(?<=上映日期: ).+?(?=\n)', info.text)[0]
    finally:
        movie.firstplay=movie.firstplay+""
    try:
        movie.imgurl=soup.find(rel="v:image").get('src')
    except:
        movie.imgurl=""
    finally:
        movie.imgurl=movie.imgurl.replace("movie_poster_cover/lpst","photo/photo").replace(".webp",".jpg")
        urllib.urlretrieve(movie.imgurl, movie.title+".jpg")
    imgr = requests.get(imgurl)
    imgsoup = BeautifulSoup(imgr.text.encode('utf-8'), 'lxml')
    size=imgsoup.find_all('div', attrs={'class': "prop"})[0].text.strip()
    bigimg= imgsoup.find_all('div', attrs={'class': "cover"})[0].find("img")["src"].replace("thumb/public","raw/public")
    headers={'Referer':'http://movie.douban.com/'}
    saveImg1(bigimg, movie.title+"_"+size+".jpg",headers)
    try:
        movie.score = soup.find('strong', 'rating_num').text
    except:
        movie.score=""
    try:
        movie.dec = soup.find(id='link-report').text.replace("©豆瓣","").strip()
    except:
        movie.dec="未知"
    try:
        for genre in soup.findAll(property="v:genre"):
            movie.type=genre.text+','+movie.type
    except:
        movie.type="剧情"
    # movie.length=soup.find(property='v:runtime').text
    try:
        movie.length=re.findall(ur'(?<=片长: ).+?(?=\n)',info.text)[0]
    except:
        movie.length="未知"
    try:
        movie.epi=re.findall(ur'(?<=集数: ).+?(?=\n)',info.text)[0]
    except:
        movie.epi="1"
    print movie.dec
    try:
        info = soup.find('div', {'id': 'info'})
        for linebreak in info.find_all('br'):
            linebreak.extract()
        for span in info.contents:
            if isinstance(span, NavigableString): continue
            if span.contents[0]:
                if span.contents[0].string == u'导演':
                    if isinstance(span.contents[1], NavigableString):
                        movie.director = span.contents[2].text
                elif span.contents[0].string == u'主演':
                    if isinstance(span.contents[1], NavigableString):
                        movie.actor = span.contents[2].text
    except:
         movie.director=""
         movie.actor=""
    return [movie.text,movie.title,str(movie.score),movie.year,movie.director,movie.actor,movie.type,movie.epi,movie.language,movie.firstplay,movie.length,movie.area,movie.imgurl,movie.dec]
def excel_insert(sheet,moviedata,row):
    # 获取MYSQL里面的数据字段名称
    # 获取并写入数据段信息
    for col in range(0,len(moviedata)):
        sheet.write(row,col,u'%s'%moviedata[col])
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
parse(search_douban("猩球崛起3"))
# print getPinyin('猩球崛起3：终极之战')
