# -*- coding: utf-8 -*-
"""
Created on 20170113
@author: WHUER
"""

import re
import requests
import shutil
import datetime
import urlparse
import os, sys
reload(sys)
sys.setdefaultencoding('utf8')
import os, sys

readsize = 4096
path = os.getcwd()
tmp_path = path + '\\ts\\'

def join(fromdir, tofile):
    output = open(tofile, 'wb')
    parts = os.listdir(fromdir)
    parts.sort()
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj = open(filepath, 'rb')
        while 1:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
        fileobj.close()
    output.close()






def get_m3u8_filename(path):
    listfile = os.listdir(path)
    m3u8_filename = ''
    for i in xrange(len(listfile)):
        m3u8_file = re.findall('m3u8', listfile[i])  # "".join(listfile.split())
        if m3u8_file != []:
            m3u8_filename = listfile[i]
    return m3u8_filename

def get_m3u8_info(m3u8_filename):
    m3u8_info = []
    f = open(m3u8_filename)
    lines = f.readlines()
    for line in lines:
        line_info = re.findall('.*?\.ts.*', line)
        if line_info != []:
            m3u8_info.append(line_info[0])
    f.close()
    return m3u8_info

def downloader(url, savepath_filename):
    re_data = requests.get(url).content
    output = open(savepath_filename, 'wb')
    output.write(re_data)
    output.close()

##############################################################################################################
def get_m3u8_file(m3u8_url):
    vid=str(urlparse.parse_qs(m3u8_url)['vid'][0])
    downloader(m3u8_url, vid+'.m3u8')
    tslist=get_m3u8_info(vid+'.m3u8')
    for i in  xrange(len(tslist)):
        downloader(tslist[i], path+'\\ts\\' + vid+"_"+str(i)+'.ts')
        m3u8file = open(vid+'.m3u8', 'w+')
        m3u8file.writelines(path+'\\ts\\' + vid+"_"+str(i)+'.ts')
        m3u8file.close()
    return vid


if __name__ == '__main__':
    # url=sys.argv[1]
    url="http://122.227.222.67/251/5/13/letv-uts/14/ver_00_22-1096271447-avc-2990796-aac-128000-6509660-2547631847-45476e0404f8c01c3122ea198fec5731-1492005092072.m3u8?crypt=82aa7f2e2454&b=3130&nlh=4096&nlt=60&bf=63&p2p=1&video_type=mp4&termid=0&tss=tvts&platid=5&splatid=512&its=12346168&qos=5&fcheck=0&amltag=5&mltag=5&proxy=3078830787,3078878574,611230082&lsbv=2g7&uid=2061534138.rp&keyitem=Wne1u_MCbvVKI8_TgM51eJFXewfs4uPxt0sGV1DC1PBfQTrtiLwkJTFP2K0.&ntm=1503057600&nkey=b4bdb7d4247feda60749a52a8d4a0d3c&nkey2=09ebd6b2843a90891664ffc3da9f825e&auth_key=1503057600-1-0-5-512-8eb537cb7a0a1b274eea4091628dc552&geo=CN-11-140-1&mmsid=64141091&tm=1503039447&key=1c1be771d006c0b907bb0806f2b559a3&playid=0&vtype=52&cvid=1519999059318&payff=1&p1=2&p2=21&vid=28791149&a_idx=&uuid=080027D8F8791503039458317_0&lsse=2ad9ns&cde=1054&cdeid=a0fb3fc0703e4a455291bae9597ed33c&appid=2009&cdetm=1503039747&cdekey=ffef38e7a3ca95409a45294a68a34b58&m3v=1&uidx=1&errc=0&gn=1017&ndtype=0&vrtmcd=108&buss=5&cips=122.224.131.186"
    # vid=get_m3u8_file(sys.argv[1])
    vid=get_m3u8_file(url)
