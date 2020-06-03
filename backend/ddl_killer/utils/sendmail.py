import yagmail
YAG = yagmail.SMTP( user="ddl_killer@yeah.net", password="XLIUFNFWCLLAEKVG", host='smtp.yeah.net')

def register_mail(email, uid, name, token):
    subject = u'【DDL_Killer】 注册用户验证信息'
    message = "\n".join([
        u'❤️亲爱的 {0} {1}, 欢迎使用DDL_Killer'.format(uid, name),
        u'👐请访问该链接，完成用户验证:',
        u'🔗<a href="http://ddlkiller.top/api/activate/?token={0}">DDL_Killer 注册链接</a>'.format(token),
        u'⚠️若不是您本人的操作，请忽略该封邮件',
        u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓DDL_Killer 团队'
        ])
    YAG.send(email, subject, message, None)


def edit_mail(email, uid, name, token):
    subject = u'【DDL_Killer】 修改用户个人信息'
    message = "\n".join([
        u'❤️亲爱的 {0} {1}, 您正在使用DDL_Killer个人信息修改服务'.format(uid, name),
        u'👐请访问该链接，完成个人信息修改:',
        u'🔗<a href="http://ddlkiller.top/api/activate/?token={0}">DDL_Killer 个人信息修改链接</a>'.format(token),
        u'⚠️若不是您本人的操作，请忽略该封邮件',
        u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓 DDL_Killer 团队'
        ])
    YAG.send(email, subject, message, None)
    

def participate_mail(email, uid, name): # 团队提醒邮件
    subject = u'【DDL_Killer】 团队事项提醒'
    message = "\n".join([
        u'❤️亲爱的 {0} {1}, 您在DDL_Killer中被添加了新的团队事项'.format(uid, name),
        u'请您及时前往DDL_Killer查看:',
        u'🔗<a href="http://ddlkiller.top/">DDL_Killer</a>',
        u'⚠️您收到这封邮件是因为您在DDL_Killer中开启了团队事项提醒功能。若您不想收到此类邮件，请前往“DDL_Killer个人中心->基础设置”中关闭团队事项提醒',
        u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓DDL_Killer 团队'
        ])
    YAG.send(email, subject, message, None)


def resource_mail(email, uid, name, course_name): # 共享资源提醒邮件
    subject = u'【DDL_Killer】 共享资源更新提醒'
    message = "\n".join([
        u'❤️亲爱的 {0} {1}, 您在DDL_Killer中有 <strong>{2}</strong> 课程的新的共享资源'.format(uid, name, course_name),
        u'请您及时前往DDL_Killer查看:',
        u'🔗<a href="http://ddlkiller.top/">DDL_Killer</a>',
        u'⚠️您收到这封邮件是因为您在DDL_Killer中开启了共享资源更新提醒功能。若您不想收到此类邮件，请前往“DDL_Killer个人中心->基础设置”中关闭共享资源更新提醒',
        u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓DDL_Killer 团队'
        ])
    YAG.send(email, subject, message, None)


def reset_pwd_mail(email, uid, name, code):
    subject = u'【DDL_Killer】 修改密码确认'
    message = "\n".join([
        u'亲爱的{} {},'.format(uid, name),
        u'您的重置密码验证码是：',
        u'<center><font size=10>{}</font></center>'.format(code),
        u'如果修改密码的请求不是您发出的，请无视这篇邮件。',
        u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓DDL_Killer 团队'
        ]) 
    YAG.send(email, subject, message, None)
