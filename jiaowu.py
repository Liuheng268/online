# -*- coding: cp936 -*-
import urllib2
import cookielib
import urllib
import re
import sys
#import chardet
def method_1():
    filename = 'FileCookieJar.txt'
    FileCookieJar = cookielib.LWPCookieJar(filename)
    FileCookieJar.save()
    CaptchaUrl = "http://xuanke.ncepu.edu.cn/(1e2exty1fepbceizihidfq45)/CheckCode.aspx"
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(FileCookieJar))
    picture = opener.open(CaptchaUrl).read()
    FileCookieJar.save()
    local = open('F:/Machine_learning/django/mysite/Lib/site-packages/online/static/yanzhengma.jpg', 'wb')
    local.write(picture)
    local.close()
def method_2(username,password,SecretCode):
    username = str(username)
    password = str(password)
    SecretCode = str(SecretCode)
    filename = 'FileCookieJar.txt'
    FileCookieJar = cookielib.LWPCookieJar(filename)
    PostUrl = "http://xuanke.ncepu.edu.cn/(1e2exty1fepbceizihidfq45)/default2.aspx"
    postData = {
'__VIEWSTATE': 'dDwyODE2NTM0OTg7Oz41FTT1Zh65HKJcBgAFuR7dgvVR0A==',
'txtUserName': username,
'TextBox2': password,
'txtSecretCode':SecretCode,
'RadioButtonList1': '学生',
'Button1': '',
'lbLanguage': '',
'hidPdrs': '',
'hidsc': '',
}
    str_len = 183
    for n in password:
        if n.isdigit() or n.isalpha():
            str_len += 1
        else:
            str_len += 3
    headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Content-Length':str_len,
'Content-Type':'application/x-www-form-urlencoded',
'Host':'xuanke.ncepu.edu.cn',
'Origin':'http://xuanke.ncepu.edu.cn',
'Referer':'http://xuanke.ncepu.edu.cn/(1e2exty1fepbceizihidfq45)/default2.aspx',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
}
    sat = urllib2.build_opener(urllib2.HTTPCookieProcessor(FileCookieJar))
    data = urllib.urlencode(postData)
    request = urllib2.Request(PostUrl, data, headers)
    try:
        response = sat.open(request)
        FileCookieJar.save()
        result = response.read().decode('gb2312')
        #print result
    except urllib2.HTTPError, e:
        pass

#*********************************************************
#'xm':'%C0%EE%CD%AE',
#'xm':'%C1%F5%BA%E2',
    postData1 = {
'xh':username,
'xm':'%C1%F5%BA%E2',
'gnmkdm':'N121603',
}
    headers1 = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate,sdch',
'Accept-Language':'zh-CN,zh;q=0.8',
'Connection':'keep-alive',
'Host':'xuanke.ncepu.edu.cn',
'Referer':'http://xuanke.ncepu.edu.cn/(w4ehhp55ykb34i55grlkcs45)/xs_main.aspx?xh='+'%s'%username,
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
}
    PostUrl1 = "http://xuanke.ncepu.edu.cn/(1e2exty1fepbceizihidfq45)/xskbcx.aspx?xh="+"%s"%username+"&xm=%DF%FS%SD%AE&gnmkdm=N121603"
    data1 = urllib.urlencode(postData1)
    request1 = urllib2.Request(PostUrl1, data1, headers1)
    try:
        response1 = sat.open(request1)
        result1 = response1.read()
        #print result1
        
    except urllib2.HTTPError, e:
        pass
    #print chardet.detect(result1)
    #result = result.decode('gbk').encode('utf-8')
    result1 = result1.decode('gbk').encode('utf-8')
    save_html = open ('D:/AppServ/www/mysite5/online/templates/kebiao/kebiao_%s.html'%username,'wb')
    save_html.write(result1)
    #save_html.write(result)
    save_html.close()
    #return result1

if __name__ == '__main__':
    S = method_1()
    #method_2('1151180811','11511@',S)
    method_2('1151180812','19961121lh@',S)
