from django.shortcuts import render

from project_management.forms import UserDescriptionForm
from project_management.kris.kris_views import new_task
from project_management.kris.kris_models import Task
from django.contrib.auth.models import User


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


def dashboard(request):
    # Object responsible for handling the creation of new tasks
    new_task_form = new_task(request)
    # Displaying all tasks for now; will use project tasks later
    tasks = Task.objects.all()

    return render(request, 'project_management/dashboard.html', {'new_task_form': new_task_form, 'tasks': tasks,
                                                                 'users': User.objects.all()})
