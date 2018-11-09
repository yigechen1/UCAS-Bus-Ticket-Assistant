# -*- coding: UTF-8 -*-
import urllib.parse,urllib.request
import json
import time
import datetime
import http.cookiejar
from PIL import Image
from pytesseract import *
import PIL.ImageOps

##################################################################

# Please set your own user, password and tel

# personal information
user = '201718018888888'
password = '888888'
tel = '1888888888'

# Please set route code
'''
  0001 Yanqihu—Yuquanlu 7:00
  0003 Yanqihu—Yuquanlu 13:00
  0004 Yanqihu—Yuquanlu 15:40
  0005 Yuquanlu—Yanqihu 6:30
  0006 Yuquanlu—Yanqihu 10:00
  0007 Yuquanlu—Yanqihu 15:00

  0009 Yanqihu—Yuquanlu 7:00(weekend)
  0011 Yanqihu—Yuquanlu 13:00(weekend)
  0012 Yanqihu—Yuquanlu 15:40(weekend)
  0013 Yuquanlu—Yanqihu 6:30(weekend)
  0014 Yuquanlu—Yanqihu 10:00（weekend)
  0015 Yuquanlu—Yanqihu 18:00（weekend)
'''

routecode= '0009'

# Please set booking date
bookingdate = '2018-07-14'

# timer switch. 
# 0: start program immediately
# 1: start program at 18:00
timer = 1

##################################################################

# use server jiang to send alert to wechat
# ref: http://sc.ftqq.com
def sendmegtowechat(text,desp):
    key = ''
    url = 'https://sc.ftqq.com/' + key + '.send?text='+text+'&desp='+desp
    req = urllib.request.Request(url=url)
    res = opener.open(req).read()

def initTable(threshold=140):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table

if(timer == 1):
    while(time.localtime(time.time()).tm_hour < 18 or time.localtime(time.time()).tm_min < 1):
        print(time.localtime(time.time()))
        time.sleep(1)


# cookie
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# try login until success
login = 0
while(login == 0):
    # checkcode
    url_code = 'http://payment.ucas.ac.cn/NetWorkUI/authImage'
    header_code = {
    'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection':'keep-alive',
    'Host':'payment.ucas.ac.cn',
    'Referer':'http://payment.ucas.ac.cn/NetWorkUI/outLogin',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    req_code = urllib.request.Request(url=url_code, headers=header_code)
    res_code = opener.open(req_code).read()
    code_file = open('authImage.jpeg','wb')
    code_file.write(res_code)
    code_file.close()

    # process checkcode
    im = Image.open('authImage.jpeg')
    im = im.convert('L')
    binaryImage = im.point(initTable(), '1')
    im1 = binaryImage.convert('L')
    im2 = PIL.ImageOps.invert(im1)
    im3 = im2.convert('1')
    im4 = im3.convert('L')
    box = (1, 1, 69, 19)
    im5 = im4.crop(box)
    code = pytesseract.image_to_string(im5)

    # login
    url_login = 'http://payment.ucas.ac.cn/NetWorkUI/fontuserLogin'
    postdata_login = urllib.parse.urlencode({'logintype': 'PLATFORM', 'nickName': user, 'password':password, 'checkCode':code}).encode('utf-8')
    header_login = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Content-Length':'74',
    'Content-Type':'application/x-www-form-urlencoded',
    'Host':'payment.ucas.ac.cn',
    'Origin':'http://payment.ucas.ac.cn',
    'Referer':'http://payment.ucas.ac.cn/NetWorkUI/outLogin',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    req_login = urllib.request.Request(url_login, postdata_login, header_login)
    res_login = opener.open(req_login).read().decode('utf-8')
    if('验证码输入错误' in res_login):
        print('Login fail! retrying!')
    else:
        print('Login success!')
        login = 1

# ticket
url_ticket = 'http://payment.ucas.ac.cn/NetWorkUI/reservedBusCreateOrder'
postdata_ticket = urllib.parse.urlencode({'routecode': routecode, 'payAmt': '6.00', 'bookingdate':bookingdate, 'payProjectId':'4', 'tel':tel, 'factorycode':'R001'}).encode('utf-8')
header_ticket = {
'Origin': 'http://payment.ucas.ac.cn',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
'Accept': '*/*',
'Referer': 'http://payment.ucas.ac.cn/NetWorkUI/openReservedBusInfoConfirm',
'X-Requested-With': 'XMLHttpRequest',
'Connection': 'keep-alive'
}
req_ticket = urllib.request.Request(url_ticket, postdata_ticket, header_ticket)

# buy ticket
success = 0
while (success < 1):
    try:
        # sleep 1 second
        #time.sleep(1)

        # create new request and get response
        res_ticket1 = opener.open(req_ticket).read()
        print(res_ticket1.decode('utf-8'))

        # check response
        if('ERROR' not in res_ticket1.decode('utf-8')):
            res1_json = json.loads(res_ticket1)
            if (res1_json['returncode'] == 'SUCCESS'):
                success = 1
                paymentaddress = 'http://payment.ucas.ac.cn/NetWorkUI/showUserSelectPayType25'+str(res1_json['payOrderTrade']['id'])
                print('Succeed to get ticket order, please enter the following address to finish the payment.')
                print(paymentaddress)
                sendmegtowechat('get-order',paymentaddress)

        else:
            print('Failed to get ticket order, retrying.')
    except:
        pass
