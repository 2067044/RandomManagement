from django.conf.urls import patterns, url

from project_management import views
from project_management.kris import kris_views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^dashboard', views.dashboard, name='dashboard'),
        url(r'^addProject', views.addProject, name='newProject'),
        url(r'^new_task', kris_views.new_task, name='new_task'),
        url(r'^project/(?P<project_id>[\w\-]+)/$', views.project, name='project'),
        url(r'^task/(?P<task_id>[\w\-]+)/$', kris_views.task, name="task"),
        url(r'^complete_task/', kris_views.complete_task, name="complete_task"),
        url(r'^profile/', views.profile, name='profile'),
        url(r'^approve_task/(?P<task_id>[\w\-]+)/$', kris_views.approve_task, name="approve_task"),
        url(r'^completed_tasks/', kris_views.completed_and_approved_tasks, name="completed_and_approved")
        )


