# /usr/bin/python
# -*- coding: utf_8_sig -*-
import sqlite3 as db
import json
import datetime
import sys
import yagmail
import numpy as np
import os
import traceback
import datetime
import time

YAG = yagmail.SMTP( user="ddl_killer@yeah.net", password="XLIUFNFWCLLAEKVG", host='smtp.yeah.net')
errorTitle = '⚠️ ddl_killer 错误提醒'
errorText = "😥 我们非常抱歉地告诉您，您有一个任务提醒在发送过程中出现了错误，请登陆 <a href='http://ddlkiller.top'>ddl_killer 网站查看</a>。\n\n感谢您的理解，祝学业顺利。\n\n"

def main():
    f = open('/root/BetaRepo/backend/ddl_killer/log/automail.log', 'a+')
    db_path = '/root/BetaRepo/backend/db.sqlite3'
    connect = db.connect(db_path)
    cu = connect.cursor()
    print('Python '+sys.version)
    print('Database initialized...')

    # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    current = datetime.datetime.now()
    nexttime = current + datetime.timedelta(minutes=1)
    current = current.strftime("%Y-%m-%d %H:%M:%S") 
    nexttime = nexttime.strftime("%Y-%m-%d %H:%M:%S") 
    # task = u'select user_id,task_id from ddl_killer_usertask join ddl_killer_user on ddl_killer_user.uid=ddl_killer_usertask.user_id where notification_time > \'{0}\' and notification_time < \'{1}\' and notification_alert == 1 and ddl_alert == 1 order by notification_time ASC;'.format(str(current), str(nexttime))
    task = u'select user_id,task_id from ddl_killer_usertask where notification_time > \'{0}\' and notification_time < \'{1}\' and notification_alert == 1 order by notification_time ASC;'.format(str(current), str(nexttime))
    
    result = cu.execute(task).fetchall()
    print(result)
    ########################### 第一次尝试发送邮件 ############################
    failures = {}
    for ut in result:
        email = cu.execute('select email from ddl_killer_user where uid={0} limit 1'.format(ut[0])).fetchall()[0][0]
        # print(type(email[0][0]))
        task = cu.execute('select title, category, content, ddl_time, urls, platform, course_name from ddl_killer_task where tid={0} limit 1'.format(ut[1])).fetchall()
        # title: task[0][0] 
        # category: task[0][1]
        # content: task[0][2]
        # ddl_time: task[0][3]
        # urls: task[0][4]
        # platform: task[0][5]
        # course_name: task[0][6]
        # print(task)
            
        tid = ut[1]
        fullText = {}
        fullText['emails'] = []
        fullText['title'] = '【DDL_Killer】 ddl 提醒: '
        if task[0][6] == None:
            fullText['title'] += task[0][0]
        else:
            # course_name = cu.execute('select name from ddl_killer_course where cid={0};'.format(i['course_id'])).fetchall()[0][0]
            fullText['title'] += task[0][6]
            
        print(fullText['title'])
        content = '<strong>{0}</strong>\n📓 details: {1}\n\n⏰ ddl_time: {2}\n📂 category: {3}\n '.format(task[0][0], task[0][2], task[0][3], task[0][1])
        if task[0][5] != '':
            content += '🏠 相关平台: {0}\n\n'.format(task[0][5])
        if task[0][4]!='':
            content += '<a href="{0}">🔗相关链接</a>\n\n'.format(task[0][4])
        fullText['content'] = content + '⌚ DDL_Killer 助您成为时间管理大师 ⌚\n\n'
        try:
            YAG.send(email, fullText['title'], fullText['content'])
            f.write('{0}:\n\t\tstatus: Success.\n\t\ttid: {1}\n\t\treceiver: {2}\n\n'.format(datetime.datetime.now(), tid, email))
        except Exception:
            try:
                failures[tid].append(fullText)
            except:
                failures[tid] = []
                failures[tid].append(fullText)
            f.write('{0}:\n\t\tstatus: Failed.\n\t\ttid: {1}\n\t\treceiver: {2}\n\nerror message: {3}\n\n'.format(datetime.datetime.now(), tid, email, traceback.format_exc()))
            

    ########################### 第二次尝试发送邮件 ############################
    if failures!={}:
        time.sleep(120) # 休眠120s后重新发送
    for tid in failures:
        for fullText in failures[tid]:
            try:
                YAG.send(email, fullText['title'], fullText['content'])
                f.write('{0}:\n\t\tstatus: Retry Success.\n\t\ttid: {1}\n\t\treceiver: {2}\n\n'.format(datetime.datetime.now(), tid, email))
            except Exception:
                f.write('{0}:\n\t\tstatus: Retry Failed.\n\t\ttid: {1}\n\t\treceiver: {2}\n\t\terror message: {3}\n\n'.format(datetime.datetime.now(), tid, email, traceback.format_exc()))
                YAG.send(email, errorTitle, errorText)
                YAG.send("ddl_killer@yeah.net", 'Sending Exception', "{0}:status: Retry Failed.\n\n\ttid: {1}\n\t\treceiver: {2}\n\t\terror message: {3}\n\n".format(datetime.datetime.now(), tid, email, traceback.format_exc()))

    f.close()
    # YAG.send('cookielau@foxmail.com', 'testCron', 'crontab run normally.')

if __name__ == '__main__':
    main()
