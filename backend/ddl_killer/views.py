from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import logout, login
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.db.models import Q

import json
import yagmail
import traceback

from .utils.jsDecryopt import decode as jsDecode
from .utils.jsDecryopt import create_key as create_js_pub_key
from .utils.sendmail import register_mail, edit_mail, participate_mail, resource_mail, reset_pwd_mail
from .utils.webScrap import updateFromCourse

from .models import User
from .models import Course
from .models import UserCourse
from .models import Task
from .models import UserTask
from .models import Resource
from .models import CourseResource
from .models import CourseTask
from .models import Note
from .models import CourseNote
from .models import Message
from .models import UserMessage
from .models import Report
from .models import PasswordModificationRecord

from itsdangerous import URLSafeTimedSerializer as utsr
import base64
import datetime
import random
from dateutil.relativedelta import relativedelta

class Token():
    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.b64encode(security_key.encode(encoding='utf-8'))

    def generate_validate_token(self, username):
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)


def get_security_public_key(request):
    """
    /security/pub-key

    generate temporary security key pair and get public key
    :param request:
    :return:
    """
    key = create_js_pub_key()
    response = {'code': 200, 'pub_key': key.pub_key, 'key_id': key.id}
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')


def create_user(request): #用户注册
    response={}
    try:
        print(request.body)
        data = json.loads(request.body.decode())
        check_user = User.objects.filter(uid=data["uid"])
        if check_user.exists() and check_user[0].is_active == True: # 已经注册且激活
            response['code'] = 400
            response["msg"]="The user already exists." 
            user = check_user[0]
            with open('./ddl_killer/log/account.log', 'a+') as f:
                f.write('{0} : account {1} requests for register but user already exists.\n'.format(str(datetime.datetime.now()), user.uid))

        else:
            token_confirm = Token(settings.SECRET_KEY)
            if check_user.exists():
                # A 注册了 B 的账户，现在A有密码，B有激活邮件
                # B 想注册，就要覆盖写，不然当前存储的还是 A 的密码
                user = check_user[0]
                user.name = data['name']
                user.password = jsDecode(data['password'])
                user.email = data['email']
                user.save()
            else:
                user = User.objects.create(uid = data["uid"], name = data["name"], password = jsDecode(data['password']), email = data["email"], is_active = False)

            token = token_confirm.generate_validate_token(data["uid"])
            try:
                register_mail(data['email'], data['uid'], data['name'], token)
                response['code'] = 200 # 成功发送邮件
                response["msg"] = "Success. Please check your email to activate the account." 
                with open('./ddl_killer/log/account.log', 'a+') as f:
                    f.write('{0} : account {1} requests for registration.\n'.format(str(datetime.datetime.now()), user.uid))
            except:
                response['code'] = 408
                response['msg'] = "Some error happens. Please retry later"
    except:
        traceback.print_exc()

    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

def edit_user(request):
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    try:
        data = json.loads(request.body.decode())
        uid=data['uid']
        user=User.objects.get(uid=uid)
        user.name=data["name"]
        isModify=False
        # print(data)
        if user.email != data["email"]:
            user.email=data["email"]
            user.is_active=False
            isModify=True
        if data["password"] != '':
            print('Not None')
            # user.password=jsDecode(data['password'])
            user.password = data['password']
            isModify=True
        user.save()
        if isModify:
            token_confirm = Token(settings.SECRET_KEY)
            token = token_confirm.generate_validate_token(data["uid"])
            try:
                edit_mail(data['email'], data['uid'], data['name'], token)
                response['code'] = 200 # 成功发送邮件
                response["msg"] = "Success. Please check your email to activate the account."
                logout_user(request)
                with open('./ddl_killer/log/account.log', 'a+') as f:
                    f.write('{0} : account {1} requests for user info modification.\n'.format(str(datetime.datetime.now()), uid))
            except:
                response['code'] = 408
                response['msg'] = "Some error happens. Please retry later"
        else:
            response['code'] = 200
            response['msg'] = 'No change detected.'
    except:
        traceback.print_exc()
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    

def active_user(request): 
    token = request.GET['token']
    # print(token)
    token_confirm = Token(settings.SECRET_KEY) 
    try:
        uid = token_confirm.confirm_validate_token(token)
        # print(uid)
    except:
        return HttpResponse(u'对不起，验证链接已经过期')
    try:
        user = User.objects.get(uid=uid)
    except User.DoesNotExist:
        return HttpResponse(u'对不起，您所验证的用户不存在，请重新注册')
    user.is_active = True
    user.save()
    confirm = u'验证成功，请进行登录操作。'
    with open('./ddl_killer/log/account.log', 'a+') as f:
        f.write('{0} : account {1} is activated.\n'.format(str(datetime.datetime.now()), uid))
    return HttpResponseRedirect('/#/successRedirect', {'msg':'Success.'})


def login_user(request):
    response = {}
    data = json.loads(request.body.decode())
    # print(data)
    uid = data['uid']
    check_user = User.objects.filter(uid=uid)
    if not check_user.exists():
        response['uid'] = uid
        response['name'] = ''
        response['code'] = 404
        response['msg'] = 'User Not Exists!'
    else:
        user = check_user[0]
        password = jsDecode(data['password'])
        if not check_password(password, user.password):
            response['uid'] = uid
            response['name'] = ''
            response['code'] = 401
            response['msg'] = 'User Password not match!'
        else:
            if user.is_active:
                response['uid'] = uid
                response['name'] = user.name
                response['code'] = 200
                response['msg'] = 'Success.'
            else:
                response['uid'] = uid
                response['name'] = ''
                response['code'] = 400
                response['msg'] = 'The account is not active yet. Check your email to activate it.'
    response['token'] = make_password(uid)
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

def logout_user(request):
    response = {}
    # if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
    #     response['code'] = 401
    #     response['msg'] = "Authorization failed!"
    #     return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    response['code'] = 200
    response['msg'] = 'Success.'
    # print(request.session.session_key)
    request.session.flush()
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    

def show_user(request, uid): #展示用户信息
    response = {}
    
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

    user = User.objects.get(uid=uid)
    # print(uid)
    response['msg'] = 'Success.'
    response['code'] = 200
    response["uid"] = user.uid
    response["name"] = user.name
    response["email"] = user.email
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    
    
def update_courses(request, uid): #从课程中心获取用户所选课程并同步作业及资源及通知
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    data = json.loads(request.body.decode())
    user_obj=User.objects.get(uid=uid)
    username = data['username']
    password = jsDecode(data['password'])
    # print(data['username'])
    # print(data['password'])
    data = updateFromCourse(uid, username, password)
    if data['code'] == 405:
        response['code'] = 405
        response['msg'] = "Password not match."
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    elif data['code'] == 406:
        response['code'] = 406
        response['msg'] = "Internel Error, plz try again later."
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

    ##################################### Log in success #########################################
    for d in data["courses"]:
        # print(json.dumps(d, ensure_ascii=False))

        ################################# check if new course ####################################
        course = Course.objects.filter(name=d["course_name"],teacher=d["course_teacher"])
        if course.exists():
            course=course[0]
            course_id=course.cid
        else:
            course=Course.objects.create(name=d["course_name"],teacher=d["course_teacher"])
            course_id=course.cid
        
        usercourse = UserCourse.objects.filter(user__uid=uid,course__cid=course_id)
        if not usercourse.exists():
            UserCourse.objects.create(user = user_obj, course = course)
    
        ########################### check if new CourseResource ##################################
        try:
            for res in d['resources']:
                resource = Resource.objects.filter(url=res['url'])
                if not resource.exists():
                    resource = Resource.objects.create(title = res['title'], url = res['url'], code = res['code'])
                else:
                    resource = resource[0]
                cr = CourseResource.objects.filter(course__cid=course.cid, resource__rid=resource.rid)
                if not cr.exists():
                    CourseResource.objects.create(course=course, resource=resource)
        except:
            traceback.print_exc()

        ########################### check if new CourseTask ##################################
        for ass in d['assignments']:
            # print(json.dumps(ass, ensure_ascii=False))
            ass_task = Task.objects.filter(urls=ass['urls'])
            if not ass_task.exists():
                ass_task = Task.objects.create(
                    title = ass['title'],
                    #course = course,
                    course_name = d['course_name'],
                    content = ass['content'],
                    platform = ass['platform'],
                    category = ass['category'],
                    urls = ass['urls'],
                    ddl_time = ass['ddl_time'],
                    create_time = ass['create_time']
                )
            else:
                ass_task = ass_task[0]
                if ass_task.title != ass['title']:
                    ass_task.title = ass['title']
                if ass_task.content != ass['content']:
                    ass_task.content = ass['content']
                if ass_task.ddl_time != ass['ddl_time']:
                    ass_task.ddl_time = ass['ddl_time']
                if ass_task.create_time != ass['create_time']:
                    ass_task.create_time = ass['create_time']
                ass_task.save() 
        
            ut = UserTask.objects.filter(user__uid=str(uid) ,task__tid=ass_task.tid)
            if not ut.exists():
                UserTask.objects.create(user=user_obj, task=ass_task, notification_time = ass['notification_time'], notification_alert = ass['notification_alert'], is_finished=ass['is_finished'])
            else:
                ut = ut[0]
                if ass['is_finished']:
                    ut.is_finished = ass['is_finished']
                ut.save()
            
            ct = CourseTask.objects.filter(course__cid=course.cid,task__tid=ass_task.tid)
            if not ct.exists():
                CourseTask.objects.create(course=course, task=ass_task)
        
            # what's more: the url before submiting homework and after submiting homework changed
            # therefore the originak usertask does not delete, we need to manually delete it
            # e.g. before submit: https://course.e2.buaa.edu.cn/portal/tool/a5695950-ebed-4b82-96d8-78e8bee58ab8?assignmentReference=/assignment/a/0d40488a-ec2c-4650-aef5-87b5ebb431b4/01fd8231-3ae6-45ba-bbd3-e4e74a138da8&panel=Main&sakai_action=doView_submission
            # after submit: https://course.e2.buaa.edu.cn/portal/tool/a5695950-ebed-4b82-96d8-78e8bee58ab8?submissionId=/assignment/s/0d40488a-ec2c-4650-aef5-87b5ebb431b4/01fd8231-3ae6-45ba-bbd3-e4e74a138da8/c5f95b89-c4bc-418e-864b-455103b27328&panel=Main&sakai_action=doView_grade
            try:
                if 'submissionId' in ass['urls']:
                    prefixU = ass['urls'].split('?')[0]+'?assignmentReference='
                    # print(prefixU)
                    for t in Task.objects.filter(urls__startswith=prefixU, title=ass['title']): # title must match here, prefixU only locate course but not specify homework task
                        ut = UserTask.objects.filter(user=user_obj, task=t)
                        for utt in ut:
                            utt.is_finished = True
                            utt.is_deleted = True
                            utt.save()
            except:
                traceback.print_exc()
        
        ########################### check if new CourseNote ##################################
        try:
            for note in d['notifications']:
                exist_notes = Note.objects.filter(url=note['url'])
                if exist_notes.exists():
                    this_note = exist_notes[0]
                    this_note.title = note['title']
                    this_note.time = note['time']
                    this_note.content = note['content']
                    this_note.attachments = '\n'.join(note['attachments'])
                    this_note.save()
                else:
                    this_note = Note.objects.create(title=note['title'], time=note['time'], url=note['url'], content=note['content'], attachments=note['attachments'])

                # print(this_note.title)    
                if not CourseNote.objects.filter(course__cid=course.cid, note__nid=this_note.nid).exists():
                    CourseNote.objects.create(course=course, note=this_note)
        except:
            traceback.print_exc()
    
    try:
        for exam in data['exam']:
            this_exams = Task.objects.filter(urls=exam['urls'])
            if this_exams.exists():
                this_exam = this_exams[0]
                uts = UserTask.objects.filter(user__uid=str(uid), task__tid=this_exam.tid)
                if not uts.exists():
                    UserTask.objects.create(user=user_obj, task=this_exam, notification_time=exam['notification_time'], notification_alert=True, is_finished=exam['is_finished'])
            else:
                this_exam = Task.objects.create(
                    title=exam["title"],
                    content=exam["content"],
                    category=exam["category"],
                    course_name=exam['course_name'],
                    urls=exam["urls"],
                    platform=exam["platform"],
                    ddl_time=exam["ddl_time"],
                    create_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                )
                UserTask.objects.create(user=user_obj, task=this_exam, notification_time=exam['notification_time'], notification_alert=True, is_finished=exam['is_finished'])
    except:
        traceback.print_exc()
                
    response['code'] = 200
    response['msg'] = 'Successfully Update your course info.'
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    

def show_user_courses(request, uid): #用户查看自己所选课程
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    response['code'] = 200
    response["data"]=[]
    usercourse = UserCourse.objects.filter(user__uid=uid)
    for uc in usercourse:
        course = Course.objects.get(cid=uc.course.cid)
        response["data"].append({
            "cid": course.cid,
            "course_name": course.name,
            "course_teacher": course.teacher,
            "isAdmin": uc.isAdmin
        })  
    
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

def admin_add_task(request, uid, cid): # 课程管理员为选择了所有课的人添加task
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    data = json.loads(request.body.decode())
    usercourse = UserCourse.objects.get(user__uid=uid, course__cid=cid)
    this_course = Course.objects.get(course_id=cid)
    if usercourse.isAdmin:
        if data['tid'] != -1:  # 若此项task已存在则视为修改此task的属性信息
            print('task already exists, only modify.\n')
            try:
                this_task = Task.objects.get(tid=data["tid"])
                this_task.title = data["title"]
                this_task.content = data["content"]
                this_task.platform = data["platform"]
                this_task.category = data["category"]
                this_task.urls = data["urls"]
                this_task.ddl_time = data["ddl_time"]
                this_task.save()
                response['code'] = 200
                response["msg"] = "Update success."
            except:
                traceback.print_exc()

        else:  # 不存在就创建新的task(传入的tid为-1),对应的course_name由后端自行获取
            task_obj = Task.objects.create(
                title=data["title"],
                content=data["content"],
                category=data["category"],
                course_name=this_course.name,
                urls=data["urls"],
                platform=data["platform"],
                ddl_time=data["ddl_time"],
                create_time=data["create_time"]
            )
            response['data'] = {}
            response['data']['tid'] = task_obj.tid

            CourseTask.objects.create(course=this_course, task=task_obj)    # 创建CourseTask对应关系

            all_usercourse = UserCourse.objects.filter(course__cid=cid)
            for uc in all_usercourse:   # 为所有选课的学生关联该task
                UserTask.objects.create(user=uc.user, task=task_obj, notification_alert=data['notification_alert'],
                                        notification_time=data['notification_time'], isAdmin=True)

            response['code'] = 200
            response["msg"] = "Create success."
    else:
        response['code'] = 501
        response["msg"]="Permission denied. The user is not admin."
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def add_task(request, uid): #用户个人添加task(需要选择或输入participant)，传入的json有participant一项列表存储接收者的学号,uid记录发布者(有修改权)
    response={}                   #没有course_id项也不需要修改course_id项

    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    data = json.loads(request.body.decode())
    print(data)
    if data['tid']!=-1: #若此项task已存在则视为修改此task的属性信息
        print('task already exists, only modify.\n')
        try:
            this_task=Task.objects.get(tid=data["tid"])
            usertask=UserTask.objects.get(user__uid=uid,task__tid=data["tid"],is_deleted=False)
            if usertask.isAdmin:  #验证修改权限
                this_task.title=data["title"]
                this_task.content=data["content"]
                this_task.platform=data["platform"]
                this_task.category=data["category"]
                this_task.urls=data["urls"]
                this_task.ddl_time=data["ddl_time"]
                usertask.notification_time=data["notification_time"]
                usertask.notification_alert=data["notification_alert"]
                this_task.save()
                usertask.is_finished = data['is_finished']
                usertask.repeat=data['repeat']
                usertask.save()
                response['code'] = 200
                response["msg"]="Update success."
            else: #没有权限只能修改提醒时间和是否开启提醒以及是否完成
                if this_task.title != data["title"] or this_task.content != data["content"] or this_task.platform != data["platform"] or this_task.category!=data["category"] or this_task.urls!=data["urls"] or this_task.ddl_time!=data["ddl_time"]:
                    response['code'] = 404
                    response["msg"]="Cannot modify these information."
                else: 
                    usertask.notification_time=data["notification_time"]
                    usertask.notification_alert=data["notification_alert"]
                    this_task.save()
                    usertask.is_finished = data['is_finished']
                    usertask.save()
                    response['code'] = 200
                    response["msg"]="Update success."
        except:
            traceback.print_exc()

    else: #不存在就创建新的task(传入的tid为-1),这时为个人添加task没有要对应的course
        task_obj = Task.objects.create(
            title=data["title"],
            content=data["content"],
            category=data["category"],
            urls=data["urls"],
            platform=data["platform"],
            ddl_time=data["ddl_time"],
            create_time=data["create_time"]
        )
        response['data']={}
        response['data']['tid'] = task_obj.tid
        response['not_exist_uid'] = []
        user_obj=User.objects.get(uid=uid)
        UserTask.objects.create(user=user_obj,task=task_obj,notification_alert=data['notification_alert'], notification_time=data['notification_time'],isAdmin=True, repeat=data['repeat']) #发布者有修改权
        try:
            for id in data["participant"]:
                try:
                    user_obj=User.objects.get(uid=id)

                    # 如果开启团队事项提醒，发送提醒邮件
                    if user_obj.participate_alert:
                        participate_mail(user_obj.email, id, user_obj.name)
                    
                except:
                    response['code'] = 503
                    response['msg'] = 'Some participants not exist.' 
                    response['not_exist_uid'].append(id)
                else: 
                    UserTask.objects.create(user=user_obj, task=task_obj, notification_alert=data['notification_alert'], notification_time=data['notification_time'])
        except:
            traceback.print_exc()
        if len(response['not_exist_uid'])==0:
            del response['not_exist_uid']
            response['code'] = 200
            response["msg"]="Create success."
        
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def show_user_tasks(request, uid): #用户查看自己的所有任务及ddl
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    try: 
        usertask = UserTask.objects.filter(user__uid=uid, is_deleted=False)       
        response["data"] = []
        if User.objects.filter(uid=uid).exists():
            try:
                response['code'] = 200
                for ut in usertask:
                    # print(t)
                    if ut.task.urls:
                        if "submissionId=" in ut.task.urls:
                            homework_url = ut.task.urls+"sakai_action=doView_grade"
                        elif "assignmentReference=" in ut.task.urls:
                            homework_url = ut.task.urls+"sakai_action=doView_submission"
                        else:
                            homework_url = ut.task.urls
                    else:
                        homework_url = ""
                    response["data"].append({
                        "tid": ut.task.tid,
                        "title": ut.task.title,
                        "course_name": ut.task.course_name,
                        "content": ut.task.content,
                        "platform": ut.task.platform,
                        "category": ut.task.category,
                        "repeat": ut.repeat,
                        "urls": homework_url,
                        "ddl_time": ut.task.ddl_time,
                        "notification_time": ut.notification_time,
                        "notification_alert": ut.notification_alert,
                        "create_time": ut.task.create_time,
                        'isAdmin': ut.isAdmin,
                        "is_finished": ut.is_finished
                    })   

                response["msg"]="Success."
            except:
                traceback.print_exc()
        else:
            response['code'] = 404
            response["msg"]="No tasks."
    except:
        traceback.print_exc()
        response['code'] = 500
        response['msg'] = "Internel Error"
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    
    
def show_course_tasks(request, uid, cid): #用户uid,相应课程cid
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    response['code']=200
    response['msg']='Success.'
    response['data'] =[]
    try:
            usertask = UserTask.objects.filter(user__uid=uid, is_deleted=False) #从该用户的所有task中筛选出和cid建立联系的task
            for ut in usertask:
                ct=CourseTask.objects.filter(course__cid=cid,task__tid=ut.task.tid)
                if ut.task.urls:
                     if "submissionId=" in ut.task.urls:
                         homework_url = ut.task.urls+"sakai_action=doView_grade"
                     elif "assignmentReference=" in ut.task.urls:
                         homework_url = ut.task.urls+"sakai_action=doView_submission"
                     else:
                         homework_url = ut.task.urls
                else:
                     homework_url = ""
                if ct.exists():
                    response["data"].append({
                        "tid": ut.task.tid,
                        "title": ut.task.title,
                        "course_name": ut.task.course_name,
                        "content": ut.task.content,
                        "platform": ut.task.platform,
                        "category": ut.task.category,
                        "urls": homework_url,
                        "ddl_time": ut.task.ddl_time,
                        "repeat": ut.repeat,
                        "notification_time": ut.notification_time,
                        "notification_alert": ut.notification_alert,
                        "create_time": ut.task.create_time,
                        "isAdmin:": ut.isAdmin,
                        "is_finished": ut.is_finished
                    })
    except:
        traceback.print_exc()
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    
def appoint_course_admin(request, cid, uid): #授予普通用户某门课程的管理权
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    response['code']=200
    response['msg']='Success.'
    usercourse = UserCourse.objects.filter(user__uid=uid,course__cid=cid)
    if usercourse.exists():
        if usercourse[0].isAdmin:
            response["msg"]="The user has already been the course_administor."
        else:
            uc=UserCourse.objects.get(user__uid=uid,course__cid=cid)
            uc.isAdmin=True
            uc.save()
            
            coursetasks = CourseTask.objects.filter(course__cid=cid)
            for ct in coursetasks:
                usertask=UserTask.objects.filter(user__uid=uid,task__tid=ct.task.tid)
                if usertask.exists():
                    ut = UserTask.objects.get(user__uid=uid,task__tid=ct.task.tid)
                    ut.isAdmin=True
                    ut.save()
            response["msg"]="Success."
    else:
        response["msg"]="The user did not select the course."
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
  
  
def alter_task_state(request, uid, tid):
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    try:
        usertask = UserTask.objects.filter(user__uid=uid,task__tid=tid, is_deleted=False)
        if usertask.exists():
            ut=UserTask.objects.get(user__uid=uid,task__tid=tid)
            ut.is_finished=not ut.is_finished
            ut.save()
            response['code']=200
            response["msg"]="Success."
        else:
            response['code']=404
            response["msg"]="The task of the user is not found."
    except:
        traceback.print_exc()
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def add_resources(request, uid, cid):
    response={}
    print(uid)
    print(request)
    print(cid)
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    try:
        data = json.loads(request.body.decode())
        if not UserCourse.objects.filter(user__uid=uid, course__cid=cid).exists:
            response['code'] = 404
            response['msg'] = "You have no access to this course."
        else: 
            resource_obj=Resource.objects.create(title=data["title"],url=data["url"],code=data["code"], user=User.objects.get(uid=uid))
            course_obj=Course.objects.get(cid=cid)
            CourseResource.objects.create(course=course_obj,resource=resource_obj)
            course_name = course_obj.name
            
            # 如果开启了共享资源更新提醒，发送提醒邮件
            usercourses = UserCourse.objects.filter(course__cid=cid)
            for uc in usercourses:
                if uc.user.resource_alert:
                    resource_mail(uc.user.email, uc.user.uid, uc.user.name, course_name)


            response['code']=200
            response["msg"]="Success."
    except:
        traceback.print_exc()
        response['code'] = 500
        response['msg'] = "Internel Error"
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

 
def show_course_resources(request, uid, cid):
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    try:
        if not UserCourse.objects.filter(user__uid=uid, course__cid=cid).exists:
            response['code'] = 404
            response['msg'] = "You have no access to this course."
        else:
            response['code'] = 200
            response['msg'] = 'Success.'
            response['data'] =[]
            courseresources = CourseResource.objects.filter(course__cid=cid)
            # print(cid)
            # print(resources)
            for cr in courseresources:
                if cr.resource.user:
                    sharer = cr.resource.user.name
                else:
                    sharer = ''
                response['data'].append({
                    "rid":cr.resource.rid,
                    "title":cr.resource.title,
                    "url":cr.resource.url,
                    "code":cr.resource.code,
                    'sharer':sharer
                })
    except:
        traceback.print_exc()
        response['code'] = 500
        response['msg'] = "Internel Error"
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

def show_course_notifications(request, uid, cid):
    response={}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    usercourse = UserCourse.objects.filter(course__cid=cid, user__uid=uid)
    if not usercourse.exists():
        response['code'] = 404
        response['msg'] = 'You have no access to this course.'
    else:
        coursenotes = CourseNote.objects.filter(course__cid=cid)
        response['data'] = []
        for cn in coursenotes:
            response['data'].append({
                'title': cn.note.title,
                'url': cn.note.url,
                'time': cn.note.time,
                'content': cn.note.content,
                'attachments': cn.note.attachments
            })
        response['code'] = 200
        response['msg'] = 'Success'
        
    # print(json.dumps(response, ensure_ascii=False))
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def delete_task(request, uid, tid):
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    usertask = UserTask.objects.filter(user__uid=uid, task__tid=tid)
    if usertask.exists():
        ut = usertask[0]
        if ut.is_deleted:
            response["code"] = 400
            response["msg"] = "The task is already deleted."
        else:
            ut.is_deleted=True
            ut.save()
            response["code"] = 200
            response["msg"]="Success."
    else:
        response["code"] = 401
        response["msg"]="The task of the user is not found."
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def personal_setting(request, uid): # 个人设置，如果是GET则直接返回个人设置；如果是POST则修改后返回个人设置
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    user = User.objects.get(uid=uid)
    # if user.exists():
    print(request.method)
    if request.method == "GET":
        response["code"] = 200
        response["data"] = []
        response['data'].append({
                'ddl_alert': user.ddl_alert,
                'participate_alert': user.participate_alert,
                'resource_alert': user.resource_alert
            })
    elif request.method == "POST":
        data = json.loads(request.body.decode())
        user.ddl_alert = data["ddl_alert"]
        user.participate_alert = data["participate_alert"]
        user.resource_alert = data["resource_alert"]
        user.save()
        
        response["code"] = 200
        response["data"] = []
        response['data'].append({
                'ddl_alert': user.ddl_alert,
                'participate_alert': user.participate_alert,
                'resource_alert': user.resource_alert
            })
    else:
        response["code"] = 400
        response["msg"]="Wrong request type!"
    # else:
        # response["code"] = 401
        # response["msg"]="The user does not exist!"
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def show_user_message(request, uid):
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    user = User.objects.get(uid=uid)
    
    print(request.GET.get('type'))
    response['data'] = []
    try:
        category = str(request.GET.get('type'))
        if category=="read":
            for um in UserMessage.objects.filter(user__uid=user.uid):
                m = um.message
                if um.is_read==True:
                    response['data'].append({
                        'mid': m.mid,
                        'title': m.title,
                        'content': m.content,
                        'is_read': um.is_read,
                        'category': m.category,
                        'publisher': m.publisher.name,
                        'publish_time': m.publish_time 
                    })
        elif category=="unread":
            for um in UserMessage.objects.filter(user__uid=user.uid):
                m = um.message
                if um.is_read==False:
                    response['data'].append({
                        'mid': m.mid,
                        'title': m.title,
                        'content': m.content,
                        'is_read': um.is_read,
                        'category': m.category,
                        'publisher': m.publisher.name,
                        'publish_time': m.publish_time 
                    })
        else:
            for um in UserMessage.objects.filter(user__uid=user.uid):
                m = um.message
                #print(m.category==category)
                if m.category==category:
                    response['data'].append({
                        'mid': m.mid,
                        'title': m.title,
                        'content': m.content,
                        'is_read': um.is_read,
                        'category': m.category,
                        'publisher': m.publisher.name,
                        'publish_time': m.publish_time 
	    			})
        response['code'] = 200
        response['msg'] = "Success."
    except:
        traceback.print_exc()
        response['code'] = 500
        response['msg'] = "Internal Error."
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')


def get_message_read(request, uid, mid):
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    user = User.objects.get(uid=uid)
    message = Message.objects.get(mid=mid)
    if not message:
        response['code'] = 404
        response['msg'] = "Message Not Found!"
    else:
        um = UserMessage.objects.filter(user__uid=uid, message__mid=mid)
        print(um.exists())
        if not um.exists():
            response['code'] = 404
            response['msg'] = "You have no rights to access this message!"
        else:
            um = um[0]
            um.is_read=True
            um.save()
            response['code'] = 200
            response['msg'] = "Success."
    print('return')
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')

def report_bugs(request, uid):
    response = {}
    if not request.META.get("HTTP_AUTHORIZATION") or not check_password(uid,request.META.get("HTTP_AUTHORIZATION")):
        response['code'] = 401
        response['msg'] = "Authorization failed!"
        return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    user = User.objects.filter(uid=uid)
    if not user.exists():
        response['code'] = 404
        response['msg'] = "User not exists!"
    else:
        data = json.loads(request.body.decode())
        user_obj = User.objects.get(uid=uid)
        Report.objects.create(user=user_obj, content=data["content"])
        response['code'] = 200
        response['msg'] = "Success."
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    
def create_forget_pwd_email_verify(request):
    """
    send verify email to specified account

    args:

    - uid

    :param request:
    :return:
    """
    data = json.loads(request.body.decode())
    uid = data.get('uid', None)
    if uid is None:
        return JsonResponse({'code': 400, 'msg': 'Bad arguments'},
                            json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')
    try:
        user = User.objects.get(uid=uid)
    except:
        return JsonResponse({'code': 400, 'msg': 'User not found'},
                            json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')

    response = {}
    try:
        code_range = list('0123456789abcdefghijklmnopqrstuvwxyz')
        verify_code = ''.join(random.choices(code_range, k=8))
        key_pair = create_js_pub_key()
        try:
            record = PasswordModificationRecord.objects.get(user=user)
            record.verify_code = verify_code
            record.key_pair = key_pair
            record.save()
        except:
            PasswordModificationRecord.objects.create(
                                                  user=user,
                                                  verify_code=verify_code,
                                                  key_pair=key_pair,
                                                  )
        reset_pwd_mail(user.email, user.uid, user.name, verify_code)

        response['code'] = 200  # 成功发送邮件
        response["msg"] = "Success. Please check your email to activate the account."
    except:
        response['code'] = 408
        response['msg'] = "Some error happens. Please retry later"
    return JsonResponse(response, json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')


def create_forget_pwd_reset_pub_key(request):
    """
    verify given code. if success, generate a temporary pub key

    args:

    - uid
    - verify_code

    :param request:
    :return: {key_id, pub_key}
    """
    data = json.loads(request.body.decode())
    uid = data.get('uid', None)
    verify_code = data.get('verify_code', None)

    try:
        user = User.objects.get(uid=uid)
    except:
        return JsonResponse({'code': 400, 'msg': 'User not found'},
                            json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')

    try:
        verify_record = PasswordModificationRecord.objects.filter(user=user).first()
    except:
        return JsonResponse({'code': 400, 'msg': 'record not found'},
                            json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')

    if verify_code == verify_record.verify_code:
        key_pair = verify_record.key_pair
        return JsonResponse({
            'code': 200,
            'msg': 'Success',
            'data': {'uid': uid,
                     'key_id': key_pair.id,
                     'pub_key': key_pair.pub_key}
        }, json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')
    else:
        return JsonResponse({'code': 400, 'msg': 'Verification failed'},
                        json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')


def change_user_pwd(request):
    """
    change password of specified user

    args:

    - uid
    - password: str, encrypt with pub key given by create_forget_pwd_reset_pub_key

    :param request:
    :return:
    """
    data = json.loads(request.body.decode())
    uid = data.get('uid', None)
    password = data.get('password', 'kid:0|')
    password = jsDecode(password)
    if isinstance(password, Exception):
        return JsonResponse({'code': 400, 'msg': 'Verification failed'},
                            json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')
    user = User.objects.get(uid=uid)
    user.password = password
    user.save()
    return JsonResponse({'code': 200, 'msg': 'success'},
                        json_dumps_params={'ensure_ascii': False}, charset='utf_8_sig')

def update_repeat_task(request):
    """
    execute everyday midnight 11:30pm , check whether repeat task today
    """
    try: 
        response={}
        response['data'] = []
        current = datetime.date.today() # today
        current = current.strftime("%Y-%m-%d") 
        for ut in UserTask.objects.filter(notification_time__startswith=current):
            if ut.repeat==None or ut.repeat=="" or ut.is_deleted:
                continue
            
            if ut.task.ddl_time!=None:
                new_ddl_time = datetime.datetime.strptime(ut.task.ddl_time, "%Y-%m-%d %H:%M:%S") 
            else:
                new_ddl_time = ut.task.ddl_time
            new_notification_time = datetime.datetime.strptime(ut.notification_time, "%Y-%m-%d %H:%M:%S") 
            if ut.repeat=='daily':
                new_notification_time = new_notification_time + datetime.timedelta(days=1)
                if ut.task.ddl_time!=None:
                    new_ddl_time = new_ddl_time + datetime.timedelta(days=1)
            elif ut.repeat=='weekly':
                new_notification_time = new_notification_time + datetime.timedelta(days=7)
                if ut.task.ddl_time!=None:
                    new_ddl_time = new_ddl_time + datetime.timedelta(days=7)
            elif ut.repeat=='monthly':
                new_notification_time = new_notification_time + relativedelta(months=+1)
                if ut.task.ddl_time!=None:
                    new_ddl_time = new_ddl_time + relativedelta(months=+1)
                
            new_notification_time = new_notification_time.strftime("%Y-%m-%d %H:%M:%S")
            new_ddl_time = new_ddl_time.strftime("%Y-%m-%d %H:%M:%S")
                
            new_task = Task.objects.create(
                title=ut.task.title,
                course_name=ut.task.course_name,
                content=ut.task.content,
                platform=ut.task.platform,
                category=ut.task.category,
                urls=ut.task.urls,
                ddl_time=new_ddl_time,
                create_time=ut.task.create_time
            )
                
            new_ut = UserTask.objects.create(
                user=ut.user, 
                task=new_task, 
                isAdmin=ut.isAdmin,
                is_finished=False,
                notification_time=new_notification_time,
                notification_alert=ut.notification_alert,
                is_deleted=False,
                repeat=ut.repeat
            )   
            
            response['data'].append({
                "uid": ut.user.uid,
                "user": ut.user.name,
                "tid": ut.task.tid,
                "task_name": ut.task.title,
                "repeat": ut.repeat
            })
            
    except:
        traceback.print_exc()
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
    
    
def q2ldbchange(request):
    response={}
    try:
        for ut in UserTask.objects.all():
            if ut.repeat==None:
                ut.repeat=""
                ut.save()
        response['code'] = 200
        response['msg'] = 'Success'
        pass
    except:
        traceback.print_exc()
        response['code'] = 677
        response['msg'] = 'Python Error'
    pass
    return JsonResponse(response, json_dumps_params={'ensure_ascii':False}, charset='utf_8_sig')
