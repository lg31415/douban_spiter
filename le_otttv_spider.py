#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
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
import json
import random
import base64, hashlib, urllib, time, re

#@DEPRECATED

def get_key(t):
    for s in range(0, 8):
        e = 1 & t
        t >>= 1
        e <<= 31
        t += e
    return t ^ 185025305

def calcTimeKey(t):
    ror = lambda val, r_bits, : ((val & (2**32-1)) >> r_bits%32) |  (val << (32-(r_bits%32)) & (2**32-1))
    magic = 185025305
    return ror(t, magic % 17) ^ magic
    #return ror(ror(t,773625421%13)^773625421,773625421%17)
def decode(data):
    version = data[0:5]
    if version.lower() == b'vc_01':
        #get real m3u8
        loc2 = data[5:]
        length = len(loc2)
        loc4 = [0]*(2*length)
        for i in range(length):
            loc4[2*i] = loc2[i] >> 4
            loc4[2*i+1]= loc2[i] & 15;
        loc6 = loc4[len(loc4)-11:]+loc4[:len(loc4)-11]
        loc7 = [0]*length
        for i in range(length):
            loc7[i] = (loc6[2 * i] << 4) +loc6[2*i+1]
        return ''.join([chr(i) for i in loc7])
    else:
        # directly return
        return data
def make_url(url, params):
    current_milli_time = lambda: int(round(time.time() * 1000))
    timestamp=current_milli_time()
    local_time=str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    parameters = {
                "loginTime":local_time,
                "stream":"1080p6m",
                "client":"android",
                "salesArea":"CN",
                "deviceKey":"1315b39351849LE061B2216120004719",
                "langType":"",
                "wcode":"cn",
                "audioId":"",
                "mac":"B01BD207A3E1",
                "kbpsType":"",
                "playType":"",
                "pricePackageType":"9",
                "broadcastId":"2",
                "support3d":"false",
                "langcode":"zh_cn",
                "channelid":"1",
                "timestamp":timestamp,
                "username":"letv_53450aa25bba576",
                "token":"1034129b81m31aiHbLl2TZ6dGySsnRhgRY4SUoC28pDDm2VBDFFblXOiGKdwQoSnYY24igUq",
                "userId":"36954000",
                "cntvMac":"B01BD207A3E1",
                "supportStream":"0_1_0",
                "bsChannel":"01001001000",
                "operType":"0",
                "expectDispatcherUrl":"false",
                "isFromCibn":"false",
                "terminalBrand":"letv",
                "p_devType":"2",
                "expectTS":"true",
                "terminalSeries":"Letv X3-43",
                "appVersion":"2.10.1",
                "validDate":"2019-06-23",
                "appCode":"292",
                "terminalApplication":"media_cibn",
                "videoid":"25520597",
                "sig":"9F251426F3B1EED800653C35BEE02CB7"}
    for key in params.keys():
        parameters[key] = params[key]
    # return parameters
    url = url + "?" + urllib.urlencode(parameters)
    return url
def getRtspUrl(FolderCode,ServiceID):
     #声明一个CookieJar对象实例来保存cookie
    #利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    #通过handler来构建opener
    opener = urllib2.build_opener(handler)
    opener.addheaders.append(('X-TERMINAL-ID','012104001091900024C136F347'))
    opener.addheaders.append(('X-USER-ID','147649615'))
    opener.addheaders.append(('X-USERPROFILE','03#7002#139803219###$4004$huzboss'))
    opener.addheaders.append(('User-Agent','Wasu/1.0(mwver 41582.0.0.0.10140;hwver 31393739;swver 00025002;uiver 3.59;caver 5.2.2.2)'))
    opener.addheaders.append(('X-TERMINAL-MODEL','soyeaSH176'))
    #此处的open方法同urllib2的urlopen方法，也可以传
    index = opener.open('http://utc.hzdtv.tv/index.jsp')

    # for item in cookie:
    #     print 'Name = '+item.name
    #     print 'Value = '+item.value
    AuthUrl=make_url('http://hd2.hzdtv.tv/templates/iptvtest/runtime/default/common/auth_hz.jsp',{})
    Play=opener.open(AuthUrl)
print str(int(time.time()*1000))
URL='http://api.itv.cp21.ott.cibntv.net/iptv/api/new/video/play/get.json'
parameters={}
print make_url(URL,parameters)