from django.conf.urls import patterns, url

from project_management import views
from project_management.kris import kris_views


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^dashboard', views.dashboard, name='dashboard'),
        url(r'^new_task', kris_views.new_task, name='new_task')
        )


