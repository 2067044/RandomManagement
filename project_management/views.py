from django.shortcuts import render
from project_management.forms import UserDescriptionForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse

def index(request):
    return render(request, 'project_management/welcome_page.html', {})


def addDescription(request):
    if request.method == 'POST':
        form = UserDescriptionForm(request.POST)

        if UserDescriptionForm.is_valid():
            userDescriptionForm.save(commit = False)
            return registration_completed(request)
        else:
            print UserDescriptionForm.errors
    else:
        form = UserDescriptionForm()
    return render(request, 'registration/registration_form.html', {'form': form})


    
