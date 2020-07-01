# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from requests import session
from requests.exceptions import ConnectTimeout
import urllib3
from lxml import etree
import json
import argparse
import re
import time
import datetime
import os
import re

# parser = argparse.ArgumentParser()
# parser.add_argument('--username', type=str)
# parser.add_argument('--password', type=str)
# args = parser.parse_args()

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
login_header = {
    "Host" : "e2.buaa.edu.cn",
    "Origin": "https://e2.buaa.edu.cn",
    "Referer": "https://e2.buaa.edu.cn/users/sign_in",
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
}
login_url = "https://e2.buaa.edu.cn/users/sign_in"

header = {
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

jwheader = {
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Host': 'jwxt-7001.e2.buaa.edu.cn',
    'Referer': 'https://sso-443.e2.buaa.edu.cn/login?service=https%3A%2F%2Fjwxt-7001.e2.buaa.edu.cn%3A443%2Fieas2.1%2Fwelcome',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
}

postData = {
    "utf8": "%E2%9C%93",
    "user[login]": 'account',
    "user[password]": 'password',
    "user[dymatice_code]": "unknown",
    "commit": "登录 Login",
}

queryHead = {
    "Host": "jwxt-7001.e2.buaa.edu.cn",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://jwxt-7001.e2.buaa.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "iframe",
    "Referer": "https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kscx/queryKcForXs"
}
queryData = {
    "xnxq": "2019-20202",
    "kssjd": "A"
}

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# python2 和 python3的兼容代码
try:
    # python2 中
    import cookielib
    print(f"user cookielib in python2.")
except:
    # python3 中
    import http.cookiejar as cookieliba
    print(f"user cookielib in python3.")
   
class LoginFailedException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message

def loginJiaowu(uid, account, password, s):
    resultData = {}
    postData["user[login]"]=account
    postData["user[password]"]=password
    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    sso_login_header = {
        "Host" : "sso-443.e2.buaa.edu.cn",
        "Origin": "https://sso-443.e2.buaa.edu.cn",
        "Referer": "https://sso-443.e2.buaa.edu.cn/users/login",
        'User-Agent': userAgent,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    header = {
        'User-Agent': userAgent,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    sso_login_url = "https://sso-443.e2.buaa.edu.cn/login"
    sso = s.get(sso_login_url, cookies=s.cookies, headers=header, verify=False)
    sso_login_soup = bs(sso.text, 'html.parser')
    sso_login_data = {
        'username': account,
        'password': password,
        'code': '',
        'lt': sso_login_soup.find('input', {'name':'lt'}).get('value'),
        'execution': sso_login_soup.find('input', {'name':'execution'}).get('value'),
        '_eventId': sso_login_soup.find('input', {'name':'_eventId'}).get('value'),
        'submit': sso_login_soup.find('input', {'class':'loginbtn'}).get('value'),
    }
    sso = s.post(sso_login_url, cookies=s.cookies, headers=header, data=sso_login_data, verify=False)
    print(sso.headers)
    print(s.cookies.get_dict())
    if '登录成功' in sso.text:
        print("Log in success...")
    else:
        resultData['code'] = 405
        resultData['msg'] = "Password not match."
        print("Log in failed...")
        return resultData

    try: 
        res = s.get(login_url, headers=login_header, verify=False, timeout=2)
        cookie = res.cookies
        # print("get response from ows {0}\n http status {1}\n resquest.url {2}\n".format(login_url, res.status_code, res.url))

        postData['authenticity_token']= str(etree.HTML(res.content).xpath('/html/head/meta[10]/@content')[0])
        # print(postData)
        # print("post login params to {0}\n http status {1}\n cookie : {2}\n".format(login_url, res.status_code, cookie))

        res = s.post(login_url, data = postData, headers = login_header, cookies=cookie, allow_redirects=True, verify=False)
        cookie = res.cookies
        # print("post login params to {0}\n http status {1}\n cookie : {2}\n".format(login_url, res.status_code, cookie))

    except ConnectTimeout:
        resultData['code'] = 504
        resultData['msg'] = "Internet Error, e2.buaa.edu.cn lost connection."
        print("Log in failed...")
        return resultData

    result = "青年北航" in res.text
    if not result:
        resultData['code'] = 500
        resultData['msg'] = "Internal Error."

    print("vpn log is done, result={0}".format(result))

    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    year = int(current_time.split('-')[0])
    month = int(current_time.split('-')[1])
    if month >= 1 and month <= 6:
        this_term = str(year-1)+'-'+str(year)+'学年第2学期'
    else:
        this_term = str(year)+'-'+str(year+1)+'学年第1学期'
    
    sdict=s.cookies.get_dict()
    scookie='SERVERID='+sdict['SERVERID']+"; _astraeus_session="+sdict['_astraeus_session']
    login_header['Cookie']=scookie
    print(sdict)

    redirect_header = {
        "Host" : "sso-443.e2.buaa.edu.cn",
        "Origin": "https://sso-443.e2.buaa.edu.cn",
        "Referer": "https://sso-443.e2.buaa.edu.cn/users/login?service=https%3A%2F%2Fjwxt-7001.e2.buaa.edu.cn%3A443%2Fieas2.1%2Fwelcome",
        'User-Agent': userAgent,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': '_webvpn_key='+sdict['_webvpn_key']+'; webvpn_username='+sdict['webvpn_username']+'; JSESSIONID='+sdict['JSESSIONID']+'; org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE='+sdict['org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE']+'; insert_cookie='+sdict['insert_cookie'],
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        'Upgrade-Insecure-Requests': '1'
    }
    redirect_url = 'https://sso-443.e2.buaa.edu.cn/login;jsessionid='+sdict['JSESSIONID']+'?service=https%3A%2F%2Fjwxt-7001.e2.buaa.edu.cn%3A443%2Fieas2.1%2Fwelcome'
    redirect_page = s.post(redirect_url, headers=header, data=sso_login_data, verify=False)
    if not '切换角色' in redirect_page.text:
        raise loginFailedException('Log in failed...')
    return



def getExamList(s):
    sdict = s.cookies.get_dict()
    queryHead['Referer']= "https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/welcome"
    del queryHead['Origin']
    exam_plain = s.get('https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kscx/queryKcForXs', headers=queryHead, cookies=s.cookies, verify=False)
    sdict = s.cookies.get_dict()
    queryHead['Origin']='https://jwxt-7001.e2.buaa.edu.cn'
    queryHead['Referer']= "https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kscx/queryKcForXs"
    exam_detail = s.post('https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/kscx/queryKcForXs', headers=queryHead, data=queryData, cookies=s.cookies, verify=False)

    exam_list = []
    exam_soup = bs(exam_detail.text, 'html.parser')
    for ex in exam_soup.find('div', {'class': "list"}).findAll('tr'):
        tds = ex.findAll('td')
        if tds==[]:
            continue
        start_time = tds[5].text.split("，")[0]+" "+tds[5].text.split("，")[-1].split('-')[0]+":00"
        end_time = tds[5].text.split("，")[0]+" "+tds[5].text.split("，")[-1].split('-')[-1]+":00"
        exam_list.append({
                    "title": tds[1].text,
                    "course_name": tds[2].text,
                    "platform": tds[3].text+" "+tds[4].text,
                    "category": "exam",
                    # "seat_number": tds[4].text,
                    # ddl_time: e.g. 2020-04-05 11:20:00~2020-04-05 13:20:00
                    "ddl_time": start_time+"~"+end_time,
                    # "start_time": tds[5].text.split("，")[-1].split('-')[0]+":00",
                    # "end_time": tds[5].text.split("，")[-1].split('-')[-1]+":00",
                    "notification_time": (datetime.datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")-datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
                    "urls":  tds[2].text,
                    "content": tds[1].text+" 期末集中考试，时间："+start_time+"~"+end_time,
                    "is_finished": False
                })
    return exam_list

def getScoreList(s):
    queryXq = '2020春'
    queryYear = queryXq[0:4]
    queryFest = queryXq[4:]
    festDict = {
        '秋': queryYear+'-'+str(int(queryYear)+1)+'1',
        '春': str(int(queryYear)-1)+'-'+queryYear+'2',
        '夏': str(int(queryYear)-1)+'-'+queryYear+'3'
    }
    pageXnxq = festDict[queryFest]
    scoreData = {
        'pageXnxq': pageXnxq,
        'pageBkcxbj': '',
        'pageSfjg': '',
        'pageKcmc': ''
    }
    queryHead['Referer'] = "https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj"
    cj_plain = s.post("https://jwxt-7001.e2.buaa.edu.cn/ieas2.1/cjcx/queryTyQmcj", headers=queryHead, cookies=s.cookies, data=scoreData)
    cj_total = []
    cj_soup=bs(cj_plain.text, 'html.parser')
    course_cj = cj_soup.findAll('table')[1].find('tr')
    while True:
        course_cj = course_cj.findNext('tr')
        td_lists = course_cj.findAll('td')
        if len(td_lists)!=14:
            break
        cj_result = {
            'course': td_lists[4].text,
            'credit': td_lists[7].text,
            'score': td_lists[10].text.strip()
        }
        cj_total.append(cj_result)

def updateFromJiaowu(uid, account, password):
    try:
        s = session()
        loginJiaowu(uid, account, password, s)
    except:
        resultData['exam'] = []
        resultData['code'] = 500
        resultData['msg'] = 'Log in failed...'
        return resultData

    exam_list = getExamList(s)
    score_list = getScoreList(s)
    resultData = {}
    resultData['exam'] = exam_list
    resultData['score'] = score_list
    resultData['code'] = 200
    resultData['msg'] = 'Success'
    return resultData
