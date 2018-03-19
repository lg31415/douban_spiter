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
import urllib2, httplib
import StringIO
import gzip

def get_m3u8(url):
    r = requests.get(url)
    if r.status_code != 200:
        return
    data = gzdecode(r).text.encode('utf-8')
    print data
def findUrlGzip(url):
   request = urllib2.Request(url)
   request.add_header('Accept-encoding', 'gzip')
   opener = urllib2.build_opener()
   f = opener.open(request)
   isGzip = f.headers.get('Content-Encoding')
   #print isGzip
   if isGzip :
       compresseddata = f.read()
       compressedstream = StringIO.StringIO(compresseddata)
       gzipper = gzip.GzipFile(fileobj=compressedstream)
       data = gzipper.read()
   else:
       data = f.read()
   return data
def findUrlTitle(url):
       html = findUrlGzip(url)
       html = html.lower()
       spos = html.find("<title>")
       epos = html.find("</title>")
       if spos != -1 and epos != -1 and spos < epos:
           title = html[spos+7:epos]
           title = title[:-9]
       else:
           title = ""
       return title
if __name__ == "__main__":
   url = 'http://115.238.246.29/106/35/50/letv-uts/14/ver_00_20-300549678-avc-478419-aac-32004-1400983-91065004-3935b858468c97e6187b4aa808b416ee-1419212377848.m3u8?crypt=5aa7f2e502&b=520&nlh=4096&nlt=60&bf=77&p2p=1&video_type=mp4&termid=1&tss=ios&platid=1&splatid=101&its=0&qos=3&fcheck=0&amltag=100&mltag=100&proxy=1945040412,3078849084,611247497&uid=2061534138.rp&keyitem=GOw_33YJAAbXYE-cnQwpfLlv_b2zAkYctFVqe5bsXQpaGNn3T1-vhw..&ntm=1501054200&nkey=ac67264a6dd92205e2ffdfeb21cc69df&nkey2=a03edc0984af4e29302bfc809a1079f8&auth_key=1501054200-1-0-1-101-57acc37a6edaa897a23e794607216b4b&geo=CN-11-140-1&mmsid=371719&tm=1501036044&key=7c1b6e680897a11650616b3e5e6d022c&playid=0&vtype=13&cvid=1519999059318&payff=0&m3v=1&hwtype=un&ostype=Windows7&p1=1&p2=10&p3=-&tn=0.7913937829434872&vid=401825&uuid=5FAC4D9C132F209BFBB5C6CF26CFB241AED5C81D_0&sign=letv&uidx=0&errc=0&gn=1049&ndtype=0&vrtmcd=102&buss=100&cips=122.224.131.186&r=1501036055850&appid=500'
   html = findUrlGzip(url)
   print html
