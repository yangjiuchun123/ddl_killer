
from bs4 import BeautifulSoup as bs
import requests
import urllib
from lxml import etree
import json
import argparse
import re
import os
import sys
import time as ttime
import traceback
import datetime
import numpy as np

jiaowu_url = "https://jwxt-7001.e1.buaa.edu.cn/ieas2.1/welcome"
exam_url = "https://jwxt-7001.e1.buaa.edu.cn/ieas2.1/kscx/queryKcForXs"
queryData = {
    "xnxq": "2019-20202",
    "kssjd": "A"
}
userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
queryHead = {
    "Host": "jwxt-7001.e1.buaa.edu.cn",
    "Connection": "keep-alive",
    # Content-Length: 23
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "Origin": "https://jwxt-7001.e1.buaa.edu.cn",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": userAgent,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "iframe",
    "Referer": "https://jwxt-7001.e1.buaa.edu.cn/ieas2.1/kscx/queryKcForXs"
}
login_header = {
    "Host" : "e1.buaa.edu.cn",
    "Origin": "https://e1.buaa.edu.cn",
    "Referer": "https://e1.buaa.edu.cn/users/sign_in",
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
login_url = "https://e1.buaa.edu.cn/users/sign_in"

header = {
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
def sso_login(account, password):
    s = requests.session()
    userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    sso_login_header = {
        "Host" : "sso-443.e1.buaa.edu.cn",
        "Origin": "https://sso-443.e1.buaa.edu.cn",
        "Referer": "https://sso-443.e1.buaa.edu.cn/users/login",
        'User-Agent': userAgent,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    }
    sso_login_url = "https://sso-443.e1.buaa.edu.cn/login"
    sso = s.get(sso_login_url, cookies=s.cookies, headers=sso_login_header)
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
    sso = s.post(sso_login_url, cookies=s.cookies, headers=sso_login_header, data=sso_login_data)
    return s

def updateFromCourse():
    account = "Cookie677"
    password = "Superstar*0415"
    ns = sso_login(account, password)
    cookie = ns.cookies
    try:
        exam_list = []
        exam = ns.get(jiaowu_url, cookies=cookie, headers=header) # login first
        exam = ns.post(exam_url, cookies=cookie, headers=queryHead, data=queryData) # get exam next

        # handler = urllib.request.HTTPCookieProcessor(cookie)
        # opener = urllib.request.build_opener(handler)
        # data = urllib.parse.urlencode(queryData).encode('utf-8')
        # req = urllib.request.Request(exam_url, data=data)
        # reponse = urllib.request.urlopen(req) 
        # print(response.read().decode('utf-8'))
        # print(urllib.request.urlopen(exam_url).read().decode('utf-8'))

        print(exam.status_code)
        print(exam.text)
        exam_soup = bs(exam.text, 'html.parser')
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
        total_list['exam'] = exam_list
    except:
        traceback.print_exc()

updateFromCourse()