import yagmail
YAG = yagmail.SMTP( user="ddl_killer@yeah.net", password="XLIUFNFWCLLAEKVG", host='smtp.yeah.net')

def register_mail(email, uid, name, token):
    subject = u'ddl_killer 注册用户验证信息'
    message = "\n".join([
    u'❤️亲爱的 {0} {1}, 欢迎使用ddl_killer'.format(uid, name),
    u'👐请访问该链接，完成用户验证:',
    u'🔗<a href="http://ddlkiller.top/api/activate/?token={0}">ddl_killer 注册链接</a>'.format(token),
    u'⚠️若不是您本人的操作，请忽略该封邮件',
    u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓ddl_killer 团队.'])
    YAG.send(email, subject, message, None)


def edit_mail(email, uid, name, token):
    subject = u'ddl_killer 修改用户个人信息'
    message = "\n".join([
    u'❤️亲爱的 {0} {1}, 您正在使用ddl_killer个人信息修改服务'.format(uid, name),
    u'👐请访问该链接，完成个人信息修改:',
    u'🔗<a href="http://ddlkiller.top/api/activate/?token={0}">ddl_killer 个人信息修改链接</a>'.format(token),
    u'⚠️若不是您本人的操作，请忽略该封邮件',
    u'👩‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓👨‍🎓 ddl_killer 团队.'])
    YAG.send(email, subject, message, None)
    
