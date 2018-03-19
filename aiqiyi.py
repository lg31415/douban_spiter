#! usr/bin/python
#coding=utf-8   //这句是使用utf8编码方式方法， 可以单独加入python头使用。
# -*- coding:cp936 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap['phantomjs.page.settings.userAgent'] = ('Mozilla/5.0 (iPhone; CPU iPhone OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B179 Safari/537.4 Maxthon/%s')  #根据需要设置具体的浏览器信息
driver = webdriver.PhantomJS(executable_path=r'G:\develop\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap)
driver.get("http://m.iqiyi.com/v_19rrkih1u4.html")
data = driver.page_source
print data
driver.quit()