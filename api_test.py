#! /usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json,demjson
import urllib2
url="http://uc.cdn.kaiyanapp.com/14651996309541464431356552brokenheartx264.mp4?t=1522831743&k=53d6b70176b07e6c"
accessKey="3cSL3UBBMB6APNGeULYW"
typeurl="PORN_PERSON_VIOLENCE"
btid="pukkasoft111111111112"
detectFrequency=1
requrl="http://video-api-sh.fengkongcloud.com/v2/saas/anti_fraud/video"
videoName="马赛克测试"
ip="218.108.76.14"
tokeid='lg31415'
# ,"channel":"","deviceid":"","phone":"","imei":"","mac":"","idfv":""
data={'url':url,"detectFrequency":detectFrequency,"tokenId":tokeid,"ip":ip,"videoName":videoName}
jsontxt={"accessKey":accessKey,"type":typeurl,"data":data,"btid":btid}
postdata=json.dumps(jsontxt)
# print postdata
# req = urllib2.Request(url = requrl,data =postdata)
# res_data = urllib2.urlopen(req)
# res = res_data.read()
# print json.dumps(demjson.decode(res), indent=4, sort_keys=False, ensure_ascii=False)

requestjson={"accessKey":accessKey,"btid":btid}
requestdata=json.dumps(requestjson)
requesturl="http://video-api-sh.fengkongcloud.com/v2/saas/anti_fraud/query_video"

req = urllib2.Request(url = requesturl,data =requestdata)
res_data = urllib2.urlopen(req)
res = res_data.read()
# print demjson.decode(res)
print json.dumps(demjson.decode(res), indent=4, sort_keys=False, ensure_ascii=False)
