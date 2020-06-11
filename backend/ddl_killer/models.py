from django.db import models
# django密码转换
from django.contrib.auth.hashers import make_password
import traceback


# Create your models here.
class User(models.Model):
    uid = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=20, null=False, default='user')
    password = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    is_active = models.BooleanField(default=False)   
    ddl_alert = models.BooleanField(default=True)
    participate_alert = models.BooleanField(default=False)
    resource_alert = models.BooleanField(default=False)
    
    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save()

    def __str__(self):
        return str(self.uid)


class Course(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False, default='course')
    teacher =models.CharField(max_length=50, null=False, default='teacher')


    def __str__(self):
        return self.name + ' ' + self.teacher   
   

class UserCourse(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    

    # def __str__(self):
    #     return self.user.uid + ' ' + self.course.name

    
class Task(models.Model):
    tid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    #course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, blank=True)
    course_name = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    platform = models.CharField(max_length=20, null=True, blank=True)
    category = models.CharField(max_length=20)
    urls = models.CharField(max_length=200,null=True, blank=True)
    ddl_time = models.CharField(max_length=50,null=True, blank=True)
    create_time = models.CharField(max_length=50,null=True, blank=True)
    

    def __str__(self):
        return self.title


class Resource(models.Model):
    rid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    code = models.CharField(max_length=50,null=True,blank=True)
    #course = models.ForeignKey('Course', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)
    

    # def __str__(self):
    #     return self.course.name + ' ' + self.title

class Note(models.Model):
    nid = models.AutoField(primary_key=True)
    url = models.CharField(max_length=200)
    title = models.CharField(max_length=100)
    time = models.CharField(max_length=50,null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    attachments = models.TextField(null=True, blank=True)

class Message(models.Model):
    mid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100)
    publisher = models.ForeignKey('User', on_delete=models.CASCADE)
    publish_time = models.CharField(max_length=50,null=True, blank=True)
    
class Report(models.Model):
    rid = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

class UserMessage(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

class UserTask(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)
    isAdmin = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    notification_time = models.CharField(max_length=50, null=True, blank=True)
    notification_alert = models.BooleanField(default = True)
    is_deleted = models.BooleanField(default=False)
    repeat = models.CharField(max_length=50, null=True, blank=True, default="")

    # def __str__(self):
    #     return ' '.join([self.user.uid, self.task.title, str(self.is_finished), self.notification_time, str(self.notification_alert)])

class CourseResource(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    resource = models.ForeignKey('Resource', on_delete=models.CASCADE)


class CourseTask(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    task = models.ForeignKey('Task', on_delete=models.CASCADE)

class CourseNote(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    note = models.ForeignKey('Note', on_delete=models.CASCADE)


class SecurityKeyPair(models.Model):
    created_at = models.TimeField(auto_now_add=True)
    pri_key = models.CharField(max_length=256)
    pub_key = models.CharField(max_length=256)  # save pub key for debugging


class PasswordModificationRecord(models.Model):
    verify_code = models.CharField(max_length=12)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key_pair = models.ForeignKey(SecurityKeyPair, on_delete=models.CASCADE)
