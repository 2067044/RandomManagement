from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return 'project_management/dashboard.html'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('project_management.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
)

