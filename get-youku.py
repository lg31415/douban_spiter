#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import  sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
import xlwt
import urllib,urllib2
import cookielib,json

prev_reported_download_percent = None
def download_hook(count, block_size, total_size):
    """ 接口是写死的 """
    global prev_reported_download_percent
    percent = int(count*block_size*100/total_size)
    if prev_reported_download_percent != percent:
        if percent % 5 == 0:
            sys.stdout.write('%s%%' % percent)
            sys.stdout.flush()
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
        prev_reported_download_percent = percent

def excel_insert(sheet,moviedata,row):
    for col in range(0,len(moviedata)):
       sheet.write(row,col,u'%s'%moviedata[col])

def maybe_download(url,filename, force=False):
    """ force 表示是否强制下载 """
    if force or not os.path.exists(filename):
        print('Attempting to download')
        filename, _ = urllib.urlretrieve(url, filename, reporthook=download_hook)
            # url+filename：表示文件的 url 地址，
            # filename 则为保存到本地时的文件名
        print('\nDownload completed!')
    # statinfo = os.stat(filename)
    return filename

def login(auth_url,username,password):
    #     # 登陆用户名和密码
    data = {b'username':username,
            b'password':password,
            b'submit':'Login'}
    # urllib进行编码
    post_data=urllib.urlencode(data)
    # 发送头信息
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    # 初始化一个CookieJar来处理Cookie
    cookieJar=cookielib.CookieJar()
    # 实例化一个全局opener
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    # 获取cookie
    req=urllib2.Request(auth_url,post_data,headers)
    result = opener.open(req)
    # 访问主页 自动带着cookie信息
    # result = opener.open(home_url)
    # 显示结果
    # print(result.read())
    return opener
def getshowid(keyword):
    searchurl='https://csales.jiaying.tv/mam/yk/data/show?page=0&pageSize=50&keyword='
    resulturl=searchurl+urllib.quote(keyword)
    # print resulturl
    result=login(auth_url,username,password).open(resulturl)
    res=json.load(result)
    return res['content'][0]['showId']

def getvideoid(showId):
    videoidurl='https://csales.jiaying.tv/mam/yk/data/video?showId='
    vurl=videoidurl+showId
    result=login(auth_url,username,password).open(vurl)
    res=json.load(result)
    showlist=[]
    for video in res:
        showlist.append(video['videoId'])
    return showlist
def getvideourl(videoId):
    videourl='https://csales.jiaying.tv/mam/yk/data/video/meida?videoId='
    viurl=videourl+urllib.quote(videoId)
    result=login(auth_url,username,password).open(viurl)
    res=json.load(result)
    return {'videoId':videoId,'mediaUrl':res['mediaUrl'],'category':res['category'],'duration':res['duration'],'showId':res['showId'],'sequence':res['sequence'],'title':res['title'],'thumbUrl':res['thumbUrl'],'smallThumbUrl':res['smallThumbUrl']}
auth_url = 'https://csales.jiaying.tv/mam/yk/login'
home_url = 'https://csales.jiaying.tv/mam/yk/data/show?page=0&pageSize=50&keyword=%E6%98%9F%E7%A0%94%E7%A9%B6%E9%99%A2'
username='seeyun'
password='sy_pw_321'
# for i in getvideoid(getshowid('火星研究院')):
#     # print  getvideourl(i)['mediaUrl'],getvideourl(i)['videoId']
#     # wget.download(getvideourl(i)['mediaUrl'],getvideourl(i)['videoId'])
#     maybe_download(getvideourl(i)['mediaUrl'],getvideourl(i)['videoId']+".mp4")

def writexls(input,output):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table-sheet',cell_overwrite_ok=True)
    excel_insert(sheet,["关键字","名称","videoId","文件名","类型","时长","showId","集数","专辑图片","小图片"],0)
    file = open(input)
    movie=[]
    row=1
    for line in file:
        try:
            for i in getvideoid(getshowid(line)):
                # print  getvideourl(i)['mediaUrl'],getvideourl(i)['videoId']
                # wget.download(getvideourl(i)['mediaUrl'],getvideourl(i)['videoId'])
                print i
                movie=getvideourl(i)
                maybe_download(movie['mediaUrl'],movie['videoId']+".mp4")
                movie=[line,movie['title'],movie['videoId'],movie['videoId']+".mp4",movie['category'],movie['duration'],movie['showId'],movie['sequence'],movie['thumbUrl'],movie['smallThumbUrl']]
                excel_insert(sheet,movie,row)
                workbook.save(output)
                row=row+1
        except:
            excel_insert(sheet,[line],row)
        finally:
            row=row+1
            workbook.save(output)
            file.close()
if __name__=='__main__':
    writexls(sys.argv[0],sys.argv[1])
    # writexls("movies","1.xls")