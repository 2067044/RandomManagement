from django.conf.urls import patterns, url

from project_management import views
from project_management.kris import kris_views



urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^dashboard', views.dashboard, name='dashboard'),
                       url(r'^addProject', views.addProject, name='newProject'),
                       url(r'^new_task/(?P<project_id>[\w\-]+)/$', kris_views.new_task, name='new_task'),
                       url(r'^project/(?P<project_slug>[\w\-]+)/$', views.project, name='project'),
                       url(r'^end_project/(?P<project_id>[\w\-]+)/$', views.end_project, name="end_project"),
                       url(r'^project_details/(?P<project_id>[\w\-]+)/$', views.project_details, name="project_details"),
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
                       url(r'^remove_admin/$', views.remove_admin, name="remove_admin"),
                       url(r'^remove_member/$', views.remove_member, name="remove_member"),
                       url(r'^promote_member/$', views.promote_member, name="promote_member"),
                       url(r'^demote_admin/$', views.demote_admin, name="demote_admin"),
                       url(r'^delete_task/(?P<task_id>[\w\-]+)/$', kris_views.delete_task,
                           name="delete_task"),
                       url(r'^new_message/(?P<task_id>[\w\-]+)/$', kris_views.new_message, name = 'new_message'),
                       url(r'^add_file/task/(?P<task_id>[\w\-]+)/$', kris_views.add_file, name = 'add_file'),
                       url(r'^add_global_file/project/(?P<project_id>[\w\-]+)/$', kris_views.add_global_file, name = "add_global_file"),
                       url(r'^message/(?P<message_id>[\w\-]+)/$', kris_views.message, name = "message"),
                       url(r'^project/(?P<project_slug>[\w\-]+)/completed_tasks/',
                           kris_views.completed_and_approved_tasks, name="completed_and_approved"),
                       )


