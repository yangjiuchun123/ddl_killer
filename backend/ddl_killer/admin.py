from django.contrib import admin
from .models import *
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['uid', 'name', 'email']
    search_fields = ['uid', 'name', 'email']


class TaskAdmin(admin.ModelAdmin):
    list_display = ['tid', 'title', 'course_name', 'platform', 'category', 'ddl_time']
    search_fields = ['tid', 'title', 'course_name', 'platform']

    # def get_course_name(self, obj):
    #     return obj.course_name
    # get_course_name.short_description = u'COURSE NAME'

    # def get_course_teacher(self, obj):
    #     if obj.course is None:
    #         return ' '
    #     else:
    #         return obj.course.teacher
    # get_course_teacher.short_description = u'COURSE TEACHER'


class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'url']
    search_fields = ['title', 'url']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['teacher', 'name']
    search_fields = ['teacher', 'name']


class UsertaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'task', 'get_course_name', 'notification_time', 'notification_alert', 'is_finished', 'isAdmin', 'is_deleted', 'repeat']
    search_fields = ['user__uid', 'task__title', 'task__course_name']

    def get_course_name(self, obj):
        if obj.task is not None:
            return obj.task.course_name
        else:
            return ' '
    get_course_name.short_description = u'COURSE NAME'

    # def get_course_teacher(self, obj):
    #     if obj.task is not None and obj.task.course is not None:
    #         return obj.task.course.teacher
    #     else:
    #         return ' '
    # get_course_teacher.short_description = u'COURSE TEACHER'

class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'time', 'content', ]
    search_fields = ['title', 'content']

    def get_note_course(self, obj):
        cn = CourseNote.objects.filter(note=obj)
        if cn.exists():
            cn = cn[0]
            return cn.course.name
        else:
            return ' '
        
class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'content']
    search_fields = ['user__uid', 'content']

class CourseNoteAdmin(admin.ModelAdmin):
    # list_display = ['task__title', 'course__name', 'task__content']
    # search_fields = ['task__title', 'course__name', 'task__content']
    pass

class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_course_name', 'get_course_teacher']
    search_fields = ['user__uid', 'course__name', 'course__teacher']

    def get_course_name(self, obj):
        if obj.course is None:
            return ' '
        else:
            return obj.course.name
    get_course_name.short_description = u'COURSE NAME'

    def get_course_teacher(self, obj):
        if obj.course is None:
            return ' '
        else:
            return obj.course.teacher
    get_course_teacher.short_description = u'COURSE TEACHER'


class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ['get_course_name', 'get_resource_title', 'get_resource_url']
    search_fields = ['course__name', 'resource__title', 'resource__url']

    def get_course_name(self, obj):
        if obj.course is None:
            return ' '
        else:
            return obj.course.name
    get_course_name.short_description = u'COURSE NAME'

    def get_resource_title(self, obj):
        if obj.resource is None:
            return ' '
        else:
            return obj.resource.title
    get_resource_title.short_description = u'RESOURCE TITLE'

    def get_resource_url(self, obj):
        if obj.resource is None:
            return ' '
        else:
            return obj.resource.url
    get_resource_url.short_description = u'RESOURCE URL'


class CourseTaskAdmin(admin.ModelAdmin):
    list_display = ['get_course_name', 'get_task_title']
    search_fields = ['course__name', 'task__title']

    def get_course_name(self, obj):
        if obj.course is None:
            return ' '
        else:
            return obj.course.name
    get_course_name.short_description = u'COURSE NAME'

    def get_task_title(self, obj):
        if obj.task is None:
            return ' '
        else:
            return obj.task.title
    get_task_title.short_description = u'TASK TITLE'

admin.site.register(User, UserAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Note, NoteAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(UserTask, UsertaskAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(CourseResource, CourseResourceAdmin)
admin.site.register(CourseTask, CourseTaskAdmin)
admin.site.register(CourseNote, CourseNoteAdmin)
admin.site.register(Message)
admin.site.register(UserMessage)

