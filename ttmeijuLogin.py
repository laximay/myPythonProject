#!/usr/bin/python
#-*- coding:utf-8 -*-

# 模拟登录天天美剧，并进入到用户页面


import urllib.parse
import urllib.request
import http.cookiejar
import sys
import re
from bs4 import BeautifulSoup



class Ttmeiju:

    cj = http.cookiejar.CookieJar()
    is_login = False
    username = ""
    password = ""


    def __init__(self, username, password):
        self.username = username
        self.password = password


    def login(self):
        print (sys.getfilesystemencoding())
        url = "http://www.ttmeiju.com/index.php/user/login.html"
        postdata =urllib.parse.urlencode({
        "username":"laximay",
        "password":"ttmeiju1122",
        "cookietime":"315360000"
        }).encode('utf-8')
        header = {
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"utf-8",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"www.ttmeiju.com",
        "Referer":"http://www.ttmeiju.com/",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
        }

        req = urllib.request.Request(url,postdata,header)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        print ("正在登录天天美剧。。。。")
        f = opener.open(req)
        f.read()
        url = "http://www.ttmeiju.com/index.php/user/myrss.html"
        print ("正在进入个人主页。。。")
        f = opener.open(url)
        data = f.read()
        type = sys.getfilesystemencoding() #转换成本地系统编码 重要代码！！

        data = data.decode(type)

        return data





tt = Ttmeiju("laximay", "ttmeiju1122")
doc = tt.login()
soup = BeautifulSoup(doc,'html.parser')
seedtable = soup.html.body.find('table',{'class','seedtable'})

print(seedtable.find_all(href=re.compile("pan.baidu."))[0].parent)

trlist = seedtable.find_all('tr')

for i in range(2,len(trlist)):
    print(1,trlist[i])



