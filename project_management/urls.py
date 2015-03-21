from django.conf.urls import patterns, url

from project_management import views
from project_management.kris import kris_views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^dashboard', views.dashboard, name='dashboard'),
        url(r'^addProject', views.addProject, name='newProject'),
        url(r'^new_task/(?P<project_id>[\w\-]+)/$', kris_views.new_task, name='new_task'),
        url(r'^project/(?P<project_slug>[\w\-]+)/$', views.project, name='project'),
        url(r'^task/(?P<task_id>[\w\-]+)/$', kris_views.task, name="task"),
        url(r'^complete_task/(?P<task_id>[\w\-]+)/$', kris_views.complete_task, name="complete_task"),
        url(r'^profile/', views.profile, name='profile'),
        url(r'^approve_task/(?P<task_id>[\w\-]+)/$', kris_views.approve_task, name="approve_task"),
        url(r'^find_task/$', kris_views.search_for_tasks, name="find_task"),
        url(r'^accept_invitation/(?P<project_invitation_id>[\w\-]+)/$',
            views.accept_invitation, name="accept_invitation"),
        url(r'^decline_invitation/(?P<project_invitation_id>[\w\-]+)/$',
            views.decline_invitation, name="decline_invitation"),
        url(r'^send_invitation/$', views.send_invitation, name="send_invitation"),
#----- Konstatin----------
        url(r'^new_message(?P<task_id>[\w\-]+)/$', kris_views.new_message, name = 'new_message'),
#-----
        url(r'^project/(?P<project_slug>[\w\-]+)/completed_tasks/',
            kris_views.completed_and_approved_tasks, name="completed_and_approved"),
        url(r'^get_tasks/', kris_views.get_offset_task_json, name="offset_task")

        )


