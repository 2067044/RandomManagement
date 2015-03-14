from django.shortcuts import render

from project_management.forms import UserDescriptionForm, ProjectForm
from project_management.kris.kris_views import new_task
from project_management.kris.kris_models import Task
from django.contrib.auth.models import User
from datetime import date


def index(request):
    return render(request, 'project_management/welcome_page.html', {})


##def addDescription(request):
##    if request.method == 'POST':
##        form = UserDescriptionForm(request.POST)
##
##        if UserDescriptionForm.is_valid():
##            userDescriptionForm.save(commit = False)
##            return registration_completed(request)
##        else:
##            print UserDescriptionForm.errors
##    else:
##        form = UserDescriptionForm()
##    return render(request, 'registration/registration_form.html', {'form': form})


def dashboard(request):
    # Object responsible for handling the creation of new tasks
    new_task_form = new_task(request)
    # Displaying all tasks for now; will use project tasks later
    tasks = Task.objects.all()
    # This determines which css style will be used in the template
    # Tasks which are more than 9 days due are alright; 4 to 9 is kinda bad;
    # less than 3 is critical
    # format: task: [{task:task, colouring:css}]
    tasks_and_colouring = []
    current_date = date.today()
    for task in tasks:
        if (task.due_date - current_date).days >= 10:
            tasks_and_colouring.append({'task': task, 'colouring': 'task-panel-normal-colour'})
        elif 3 < (task.due_date - current_date).days < 10:
            tasks_and_colouring.append({'task': task, 'colouring': 'task-panel-attention-colour'})
        else:
            tasks_and_colouring.append({'task': task, 'colouring': 'task-panel-critical-colour'})
    return render(request, 'project_management/dashboard.html',
                  {'new_task_form': new_task_form,
                   'tasks': tasks_and_colouring,
                   'users': User.objects.all(),
                   })


def addProject(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner=request.user
            project.save()
            return render(request,'project_management/project.html',{'project': project})
        else:
            return redirect('/dashboard/')
    else:
        form = ProjectForm()
    return form


def project(request):
    return redirect('/dashboard/')

    # This determines which css style will be used in the template
    # Tasks which are more than 9 days due are alright; 4 to 9 is kinda bad;
    # less than 3 is critical
    # format: task: [{task:task, colouring:css}]
    tasks_and_colouring = []
    current_date = date.today()
    for task in tasks:
        if (task.due_date - current_date).days >= 10:
            tasks_and_colouring.append({'task': task, 'colouring': 'task-panel-normal-colour'})
        elif 3 < (task.due_date - current_date).days < 10:
            tasks_and_colouring.append({'task': task, 'colouring': 'task-panel-attention-colour'})
        else:
            tasks_and_colouring.append({'task': task, 'colouring': 'task-panel-critical-colour'})
    return render(request, 'project_management/dashboard.html',
                  {'new_task_form': new_task_form,
                   'tasks': tasks_and_colouring,
                   'users': User.objects.all(),
                   })
