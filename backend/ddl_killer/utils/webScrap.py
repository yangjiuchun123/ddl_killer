# -*- coding: utf-8 -*-
# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'
# Server Version

from bs4 import BeautifulSoup as bs
import requests
import urllib3
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
# from . import PasswordException

# parser = argparse.ArgumentParser()
# parser.add_argument('--username', type=str)
# parser.add_argument('--password', type=str)
# args = parser.parse_args()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# python2 和 python3的兼容代码
try:
    # python2 中
    import cookielib
    # print(f"use cookielib in python2.")
except:
    # python3 中
    import http.cookiejar as cookieliba
    # print(f"use cookielib in python3.")

userAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
login_header = {
    "Host" : "e2.buaa.edu.cn",
    "Origin": "https://e2.buaa.edu.cn",
    "Referer": "https://e2.buaa.edu.cn/users/sign_in",
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}
login_url = "https://e2.buaa.edu.cn/users/sign_in"

header = {
    'User-Agent': userAgent,
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
}

recrusiveHeader = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Origin': 'https://course.e2.buaa.edu.cn',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.24 Safari/537.36 Edg/83.0.478.18',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'iframe',
    'Referer': '',
}

isDebug = True

class PasswordException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message


def getFolderList(rr):
    # rr = beautifulSoup(session.get(assignment_iframe_url, cookies=cookie).text, 'html.parser')
    folders = [i.text.strip() for i in rr.findAll('a', {'title': '文件夹'})]
    folders.pop(0)
    # print('Folder List: {0}'.format(str(folders)))
    return folders

def getCollectionIdPrefix(rr):
    # rr = beautifulSoup(session.get(assignment_iframe_url, cookies=cookie).text, 'html.parser')
    for script in rr.findAll(attrs={'type':"text/javascript"}):
        # print(str(script))
        if 'collectionId' in str(script):
            content = str(script)
            break
    # print(content)
    pattern = re.compile('collectionId = (\S+);')
    prefix = pattern.findall(content)[0][1:-1]
    return prefix

def getCsrfToken(rr):
    # rr = beautifulSoup(session.get(assignment_iframe_url, cookies=cookie).text, 'html.parser')
    return rr.find('input',{'name':'sakai_csrf_token'}).attrs['value']

def enterFolder(collectionId, ass_iframe_url, s, cookie, token):
    # enter is bidirectional, both go deepin and return 
    ## mock navigate data
    # print('Enter Folder: {0}'.format(collectionId))
    data = {
        'source': 0,
        'collectionId': collectionId,
        'navRoot': '',
        'criteria': 'title',
        'sakai_action': 'doNavigate',
        'sakai_csrf_token': token
    }
    # 回到主目录需要特判
    if collectionId.count('/')==3:
        data['navRoot'] = collectionId
    ## go to next folder
    s.post(ass_iframe_url, cookies=cookie, data=data)
    # s.get(ass_iframe_url, cookies=cookie)
    return

def getResUnderFolder(prefix, ass_iframe_url, s, cookie, token):
    # Before Action: enter son folder
    # print('Getting Resources under path: {0}'.format(prefix))
    rr = bs(s.get(ass_iframe_url, cookies=cookie).text, 'html.parser')
    # print("Location: {0}".format(rr.find('div', {'class':"breadCrumb specialLink"}).text.strip().replace('\t','').replace('\r','').replace('\n','')))
    # print('Folders {0} under the path.'.format(str(getFolderList(rr))))
    collection = [i for i in rr.findAll('a') if i.get('href')!=None and i.get('href').startswith('http') and i.text.strip()!='']
    res = []
    for i in collection:
        single_res = {}
        single_res['title'] = i.text.strip()
        single_res['url'] = i.get('href')
        single_res['code'] = ''
        # print(single_res)
        res.append(single_res)
    
    res.extend(collectAllFolderRes(rr, prefix, ass_iframe_url, s, cookie, token))
    # res = np.unique(res)

    return res
    
def collectAllFolderRes(rr, prefix, ass_iframe_url, s, cookie, token):
    # Before Action: has beautifulSoup content to get folder list
    res = [] 
    folders = getFolderList(rr)
    if len(folders)!=0:
        for littleFolder in folders:
            # ports = prefix.split('/')[2:]
            # for i in range(0, len(ports)):
            #     print(ports[i])
            #     if ports[i] in folders:
            #         prefix = prefix.split(ports[i])[0]
            #         enterFolder(prefix, ass_iframe_url, s, cookie, token)
            #         continue
            # if littleFolder in prefix:
            #     prefix = prefix.split(littleFolder)[0]
            #     enterFolder(prefix, ass_iframe_url, s, cookie, token)
            #     break
            currentdir = prefix.split('/')[-2]
            if currentdir in folders:
                break
            collectionId=prefix+littleFolder+'/'
            enterFolder(collectionId, ass_iframe_url, s, cookie, token) 
            littleRes = getResUnderFolder(collectionId, ass_iframe_url, s, cookie, token)
            res.extend(littleRes)
            enterFolder(prefix, ass_iframe_url, s, cookie, token)
    
    return res

def updateFromCourse(uid, account, password):
    startTime = datetime.datetime.now()
    # path=os.path.realpath(__file__)
    # print(path)
    # print(os.getcwd())
    # print(os.path.join(os.getcwd(), 'ddl_killer/log/webScrap.log'))

    try:
        s = requests.session()
        if isDebug:
            print("开始模拟登录")
        postData = {
            "utf8": "%E2%9C%93",
            "user[login]": account,
            "user[password]": password,
            "commit": "登录 Login",
        }

        res = s.get(login_url, headers=login_header, verify=False)
        cookie = res.cookies
        # if isDebug:
        #     print("get response from ows {0}\n http status {1}\n resquest.url {2}\n".format(login_url, res.status_code, res.url))

        postData['authenticity_token']= str(etree.HTML(res.content).xpath('/html/head/meta[10]/@content')[0])
        # if isDebug:
        #     print("post login params to {0}\n http status {1}\n cookie : {2}\n".format(login_url, res.status_code, cookie))

        res = s.post(login_url, data = postData, headers = login_header, cookies=cookie, allow_redirects=True, verify=False)
        cookie = res.cookies
        # if isDebug:
        #     print("post login params to {0}\n http status {1}\n cookie : {2}\n".format(login_url, res.status_code, cookie))

        # 获得当前学期时间
        current_time = ttime.strftime("%Y-%m-%d %H:%M:%S", ttime.localtime())
        year = int(current_time.split('-')[0])
        month = int(current_time.split('-')[1])
        if month >= 1 and month <= 6:
            this_term = str(year-1)+'-'+str(year)+'学年第2学期'
        else:
            this_term = str(year)+'-'+str(year+1)+'学年第1学期'

        if isDebug:  
            print('Checking '+this_term)
            print("初始化完成...")


        
        course_url = "https://course.e2.buaa.edu.cn/portal/login"

        course = s.get(course_url, cookies=cookie, headers=header, allow_redirects=True)
        if isDebug:
            print("status code: " + str(course.status_code))
        course_doc = course.text
        soup = bs(course_doc, 'html.parser')
        # print(soup.prettify())
        if (soup.find(id="loginLink1") == None or soup.find(id="loginLink1").text=='登陆'):
            raise PasswordException('Wrong')
        else:
            print('{0} {1} Log in course Successfully.'.format(str(uid), account))
        
        course_list = {}
        links = soup.findAll('li')
        for link in links:
            try:
                if (link.a.span.get('class')[0] == 'fullTitle'):
                    course_list[link.a.span.text.strip()] = link.a.get('href')
            except:
                if link.get('class')!=None and link.get('class')[0] == 'nav-menu':
                    course_list[link.text.strip()] = link.a.get('href')

        # if isDebug:  
        #     print(course_list)

        try:
            del course_list['我的工作空间']
        except:
            pass
        
        print("Course info generated...")

        
        total_list = {}
        total_list['courses'] = []
        for course_name, url in course_list.items():
            single_list = {}
            single_list['course_name'] = course_name
            if isDebug:  
                print(course_name, url) # get all course urls
            cc = s.get(url, cookies=cookie, headers = header)
            if (cc.status_code != 200):
                if isDebug:  
                    print("Error in getting " + course_name)
            menus = bs(cc.text, 'html.parser').findAll('a', {'class':'toolMenuLink'})
            get_info = False
            get_res = False
            get_ass = False
            get_note = False
            for i in menus:
                if i.text.strip()=='站点信息':
                    info_url = i.get('href')
                    if info_url == None:
                        info_url = url
                    get_info = True
                    info_soup = bs(s.get(info_url, cookies=cookie, headers=header).text, 'html.parser') # information_soup
                    info_detail_url = info_soup.find('div', {'class':'portletMainWrap'}).iframe.get('src')
                if i.text.strip()=='资源':
                    resource_url = i.get('href')
                    if resource_url == None:
                        resource_url = url
                    get_res = True
                    res_soup = bs(s.get(resource_url, cookies=cookie, headers=header).text, 'html.parser') # rescourses_soup
                    doc_url = res_soup.find('div', {'class':'portletMainWrap'}).iframe.get('src')
                if i.text.strip()=='作业':
                    assignment_url = i.get('href')
                    if assignment_url == None:
                        assignment_url = url
                    get_ass = True
                    ass_soup = bs(s.get(assignment_url, cookies=cookie, headers=header).text, 'html.parser') # assignment_soup
                    homework_url = ass_soup.find('div', {'class':'portletMainWrap'}).iframe.get('src')
                if i.text.strip()=='通知':
                    notification_url = i.get('href')
                    if notification_url == None:
                        notification_url = url
                    get_note = True
                    not_soup = bs(s.get(notification_url, cookies=cookie, headers=header).text, 'html.parser') # notification_soup
                    note_url = not_soup.find('iframe').get('src')

                    

                
            ############################## get info ###############################################

            if get_info:
                # info_soup = bs(s.get(info_url, cookies=cookie, headers=header).text, 'html.parser') # information_soup
                # info_detail_url = info_soup.find('div', {'class':'portletMainWrap'}).iframe.get('src')
                if isDebug:  
                    print("info_iframe_page: " + info_detail_url)
                info_content = s.get(info_detail_url, cookies=cookie, headers=header)
                info_ss = bs(info_content.text, 'html.parser')
                course_term = info_ss.find('div', {'class':"portletBody specialLink"}).findAll('td')[0]
                # 已解决，类型不同导致的判断出错
                # (type(course_term)) # <class 'bs4.element.Tag'>
                # (type(this_term)) # <class 'str'>
                if str(course_term.text).strip() != this_term:
                    if isDebug:  
                        print("Course {0} not in this term...".format(course_name))
                    continue
                    
                course_teacher = info_ss.find('div', {'class':"portletBody specialLink"}).findAll('td')[2].text.strip().split(',')[0]
                single_list['course_teacher'] = course_teacher
            else:
                single_list['course_teacher'] = 'teacher'

            ############################## get resources ##########################################
            
            if get_res:
                # res_soup = bs(s.get(resource_url, cookies=cookie, headers=header).text, 'html.parser') # rescourses_soup
                # doc_url = res_soup.find('div', {'class':'portletMainWrap'}).iframe.get('src')

                if isDebug:  
                    print('res_iframe_page: ' + doc_url)
                res_content = s.get(doc_url, cookies=cookie)
                
                res_ss=bs(res_content.text, 'html.parser')
                
                # res_lists = []
                # for i in res_ss.find('div').find('form').findAll('tr'):
                #     single_res = {}
                #     if ("https" in i.findAll('a')[1].get('href') and i.findAll('a')[1].text.strip() != ""):
                #         single_res['title'] = i.findAll('a')[1].text.strip()
                #         single_res['url'] = i.findAll('a')[1].get('href')
                #         single_res['code'] = ''
                #         res_lists.append(single_res)
                # single_list['resources'] = res_lists
                        
                prefix = getCollectionIdPrefix(res_ss)
                token = getCsrfToken(res_ss)
                print(prefix)
                print(token)
                single_list['resources'] = getResUnderFolder(prefix, doc_url, s, cookie, token)
                

            else:
                single_list['resources'] = []

            ############################### get assignments #######################################
            
            if get_ass:
                # ass_soup = bs(s.get(assignment_url, cookies=cookie, headers=header).text, 'html.parser') # assignment_soup
                # homework_url = ass_soup.find('div', {'class':'portletMainWrap'}).iframe.get('src')

                if isDebug:  
                    print("assignment_iframe_page: " + homework_url)
                ass_content = s.get(homework_url, cookies=cookie)
                
                ass_ss=bs(ass_content.text, 'html.parser')
                
                ass_lists = []
                
                if ass_ss.find('div').find('p')==None:
                    for i in ass_ss.find('div').findAll('form')[5].findAll('tr'):
                        if (i.find("a") != None and "https" in i.find('a').get('href') and i.find('a').text.strip()!=""):
                            ass = {}
                            ass['title'] = i.findAll('td')[1].text.strip()

                            ################ create_time #######################
                            if len(i.findAll('td')) > 3:
                                date = i.findAll('td')[3].text.strip()
                            else:
                                date = ''
                            offset = 0
                            if '下午' in date:
                                time = int(date.split(' ')[1].split(':')[0].split('下午')[1])
                                if time == 12:
                                    offset = 0
                                else: 
                                    offset = 12
                                ass['create_time'] = date.split(' ')[0]+' '+str(int(date.split(' ')[1].split(':')[0].split('下午')[1])+offset) + ':' + date.split(':')[1]+':00'
                            elif '上午' in date:
                                time = int(date.split(' ')[1].split(':')[0].split('上午')[1])
                                if time == 12:
                                    offset = -12
                                else: 
                                    offset = 0
                                ass['create_time'] = date.split(' ')[0]+' '+str(int(date.split(' ')[1].split(':')[0].split('上午')[1])+offset) + ':' + date.split(':')[1]+':00'
                            else:
                                ass['create_time'] = None


                            ################ ddl_time #######################

                            if len(i.findAll('td')) > 4:
                                date = i.findAll('td')[4].text.strip()
                            else:
                                date = ''
                            ass['platform'] = '课程中心'
                            if '计算机网络实验' in course_name:
                                ass['platform'] = ass['platform']+" & 中国大学慕课"
                            ass['category'] = 'homework'
                            offset = 0
                            if '下午' in date:
                                time = int(date.split(' ')[1].split(':')[0].split('下午')[1])
                                if time == 12:
                                    offset = 0
                                else: 
                                    offset = 12
                                ass['ddl_time'] = date.split(' ')[0]+' '+str(int(date.split(' ')[1].split(':')[0].split('下午')[1])+offset) + ':' + date.split(':')[1]+':00'
                            elif '上午' in date:
                                time = int(date.split(' ')[1].split(':')[0].split('上午')[1])
                                if time == 12:
                                    offset = -12
                                else: 
                                    offset = 0
                                ass['ddl_time'] = date.split(' ')[0]+' '+str(int(date.split(' ')[1].split(':')[0].split('上午')[1])+offset) + ':' + date.split(':')[1]+':00'
                            else:
                                ass['ddl_time'] = ''
                            
                            if ass['ddl_time'] != '':
                                pattern = re.compile(r'[\d]+')
                                a = re.findall(pattern, ass['ddl_time'])
                                year = int(a[0])
                                month = int(a[1])
                                day = int(a[2])
                                hour = int(a[3])
                                minute = int(a[4])
                                second = int(a[5])
                                if day==1:
                                    month = (month+11)%12
                                    if month==0:
                                        month=12
                                        year-=1
                                    day = (0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month]
                                else:
                                    day -= 1
                                ass['notification_time'] = '%d-%02d-%02d %02d:%02d:%02d'%(year, month, day, hour, minute, second)
                                ass['notification_alert'] = True
                                ass['ddl_time'] = ass['ddl_time'].split('-')[0]+'-'+'%02d'%(int(ass['ddl_time'].split('-')[1]))+'-'+'%02d'%(int(ass['ddl_time'].split('-')[2].split(' ')[0]))+' '+ass['ddl_time'].split('-')[2].split(' ')[1]
                            else:
                                ass['notification_time'] = ''
                                ass['notification_alert'] = False

                            if ass['create_time'] != None and ass['create_time'] != '':
                                ass['create_time'] = ass['create_time'].split('-')[0]+'-'+'%02d'%(int(ass['create_time'].split('-')[1]))+'-'+'%02d'%(int(ass['create_time'].split('-')[2].split(' ')[0]))+' '+ass['create_time'].split('-')[2].split(' ')[1]
                            ass['urls'] = i.find('a').get('href')
                            homework_detail = bs(s.get(ass['urls'], cookies=cookie, headers=header).text, 'html.parser')

                            try:
                                ass['content'] = homework_detail.find('div', {'class': 'textPanel'}).text
                            except:
                                ass['content'] = ''

                            little_menus = [ i.text.strip() for i in homework_detail.find('table').findAll('th') ]
                            if '历史' in little_menus:
                                ass['is_finished'] = True
                            else:
                                ass['is_finished'] = False
                            ass_lists.append(ass)
            
                single_list['assignments'] = ass_lists
            else:
                single_list['assignments'] = []



            ############################### get assignments #######################################
            if get_note:
                # not_soup = bs(s.get(notification_url, cookies=cookie, headers=header).text, 'html.parser') # notification_soup
                # note_url = not_soup.find('iframe').get('src')

                course_note_list = []

                if isDebug:
                    print('notification_iframe_page: ' + note_url)
                note_content = s.get(note_url, cookies=cookie)
                note_ss = bs(note_content.text, 'html.parser')
                token = getCsrfToken(note_ss)
                selectData = {
                    'eventSubmit_doChange_pagesize': 'changepagesize',
                    'selectPageSize': '200',
                    'sakai_csrf_token': token
                }
                returnData = {
                    'eventSubmit_doLinkcancel': '%E8%BF%94%E5%9B%9E%E5%88%B0%E7%9B%AE%E5%BD%95%E6%B8%85%E5%8D%95', # 返回目录清单
                    'sakai_csrf_token': token
                }
                s.post(note_url, cookies=cookie, data=selectData)
                note_content = s.get(note_url, cookies=cookie)
                note_ss = bs(note_content.text, 'html.parser')
                note_list = [i.a.get('href') for i in note_ss.findAll('td', {'headers':'subject'})]
                for note_each_url in note_list:
                    note_details = {}
                    not_son_content = s.get(note_each_url, cookies=cookie)
                    not_son_ss = bs(not_son_content.text, 'html.parser')
                    for j in not_son_ss.findAll('tr'):
                        if (j.th.text.strip()=='标题'):
                            note_details['title'] = j.td.text.strip()
                        if (j.th.text.strip()=='修改时间'):
                            note_details['time'] = j.td.text.strip()
                        if (j.th.text.strip()=='对象'):
                            break

                    note_details['url'] = note_each_url
                    for j in not_son_ss.findAll('h4'):
                        if j.text.strip()=='内容':
                            note_content = ''
                            for k in j.next_siblings:
                                if k.name == 'p':
                                    note_content += k.text
                                elif k.name == 'form':
                                    break
                            break

                    note_details['content'] = re.sub('\s', '', note_content)
                    # print(note_details['content'])
                    note_details['attachments'] = []
                    if not_son_ss.find('ul', {'class':'attachList'}) != None: # ul无序列表
                        for each_attach in not_son_ss.find('ul', {'class':'attachList'}).findAll('li'):
                            note_details['attachments'].append(each_attach.a.get('href'))
                    course_note_list.append(note_details)
                    s.post(note_url, cookies=cookie, data=returnData)
                    s.get(note_url, cookies=cookie)
                    # print(note_details)

                single_list['notifications'] = course_note_list
            else:
                single_list['notifications'] = []

            ############################### aggregate all stuffs #######################################
            total_list['courses'].append(single_list)



        # if isDebug:  
        #     json_dicts=json.dumps(total_list,indent=4)
        #     print(json_dicts)
        
        with open("./ddl_killer/log/courses.json", "w", encoding='utf-8') as f:
            f.write(str(json.dumps(total_list, indent=4, ensure_ascii=False)))

        total_list['code'] = 200
        endTime = datetime.datetime.now()
        print("Duration time : ")
        print(endTime - startTime)
        with open('./ddl_killer/log/webScrap.log', 'a+') as f:
            f.write('{4} {0} {1} update {2} courses in {3}\n'.format(str(uid), account, str(len(total_list['courses'])), str(endTime-startTime), str(startTime)))
    except PasswordException as e:
        print('{0} {1} Log in failed, password not match. '.format(str(uid), account))
        # print(e)
        print('=============================================')
        # print(traceback.format_exc())
        with open('./ddl_killer/log/webScrap.log', 'a+') as f:
            f.write('{0} {1} {2} password not match.\n'.format(str(startTime), str(uid), account ))

        total_list = {}
        total_list['code'] = 405
        total_list['courses'] = []
        # print('return password wrong totallist') 
        return total_list
    except Exception as e:
        print('{0} {1} Internal Error. '.format(str(uid), account))
        print(traceback.format_exc())
        print('=============================================')
        with open('./ddl_killer/log/webScrap.log', 'a+') as f:
            f.write('{0} {1} {2} Internal Error {3}.\n{4}\n'.format(str(startTime), str(uid), account, e, traceback.format_exc()))

        total_list = {}
        total_list['code'] = 406
        total_list['courses'] = []

        return total_list
    return total_list

# if __name__ == '__main__':
#     try:
#         updateFromCourse('1', account, password)
#     except KeyboardInterrupt:
#         sys.exit(0)