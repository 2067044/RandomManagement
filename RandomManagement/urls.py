from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.views.generic import RedirectView

class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        print 'function'
        return '/dashboard/'

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('project_management.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/', include('registration.backends.simple.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

