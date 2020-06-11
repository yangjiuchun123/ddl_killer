"""django_tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf.urls import url ##新增

urlpatterns = [
    path(r'user/<int:uid>/course/<int:cid>/tasks', views.show_course_tasks),
    path(r'user/<int:uid>/tasks', views.show_user_tasks),
    path(r'user/<int:uid>/course/<int:cid>/resources', views.show_course_resources),
    path(r'user/<int:uid>/course/<int:cid>/resources/new', views.add_resources),
    path(r'user/<int:uid>/courses', views.show_user_courses),
    path(r'user/<int:uid>/course/<int:cid>/tasks/new', views.admin_add_task),
    path(r'user/<int:uid>/course/<int:cid>/notifications', views.show_course_notifications),
    path(r'user/<int:uid>/tasks/new', views.add_task),
    path(r'course/<int:cid>/user/<int:uid>/appoint', views.appoint_course_admin),
    path(r'register', views.create_user),
    path(r'login', views.login_user),
    path(r'logout', views.logout_user),
    path(r'user/<int:uid>/info', views.show_user),
    path(r'user/<int:uid>/task/<int:tid>/alterTaskState', views.alter_task_state),
    path(r'activate/', views.active_user, name='active_user'),
    path(r'user/<int:uid>/update_course', views.update_courses),
    path(r'modify', views.edit_user),
    path(r'q2l/dbchange', views.q2ldbchange),
    path(r'user/<int:uid>/tasks/<int:tid>/delete', views.delete_task),
    path(r'user/<int:uid>/settings', views.personal_setting),
    path(r'security/pub-key', views.get_security_public_key),  # allow: GET
    path(r'user/<int:uid>/message', views.show_user_message),
    path(r'user/<int:uid>/message/<int:mid>/read', views.get_message_read),
    path(r'user/<int:uid>/report', views.report_bugs),
    path(r'user/forget/email', views.create_forget_pwd_email_verify),
    path(r'user/forget/verify', views.create_forget_pwd_reset_pub_key),
    path(r'user/forget/reset', views.change_user_pwd),
    path(r'update_repeat_task', views.update_repeat_task),
    
]
