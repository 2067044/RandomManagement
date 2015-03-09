from django.shortcuts import render
from project_management.forms import UserDescriptionForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return render(request, 'project_management/welcome_page.html', {})


    
