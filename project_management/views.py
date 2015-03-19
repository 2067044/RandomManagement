from django.shortcuts import render
from project_management.forms import UserDescriptionForm, ProjectForm
from project_management.models import Project, UserDescription
from django.shortcuts import redirect
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

def getUserProjects(user):
    users_projects = []
    projects = Project.objects.all()
    for project in projects:
        if (project.owner == user):
            users_projects.append(project)
    return users_projects

def dashboard(request):
    return render(request,'project_management/dashboard.html', {'user_project':getUserProjects(request.user)})


def addProject(request):
    users_projects = getUserProjects(request.user)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner=request.user
            project.save()
            return redirect('/project/{0}'.format(project.slug))
        else:
            return redirect('/dashboard/')
    else:
        form = ProjectForm()

    return render(request, 'project_management/projectForm.html', {'form':form})

def project(request, project_slug):
    project = Project.objects.get(slug=project_slug)
    users_projects = getUserProjects(request.user)

    if request.method == 'POST':
        print 'TEST 1'
        member_username = request.POST['add_user']
        print request.POST['add_user']
        if member_username.is_valid():
            new_member = User.objects.filter(username=member_username)
            project.members.add(new_member)
            project.save()
            
    return render(request,'project_management/project.html',{'project':project, 'user_project':users_projects})

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

def profile(request):
    if request.method == 'POST':
        description=UserDescriptionForm(request.POST)
        if description.is_valid() and description!= "":
            UserDescription.user=request.user
            UserDescription.description = description
            UserDescription.save()
        if UserForm.is_valid():
            password1=UserForm(request.POST['password1'])
            password2=UserForm(request.POST['password2'])
            if password1==password2:
                user=User.objects.get(id=request.user.id)
                user.set_password(password1)
                user.save()
        return render(request,'project_management/profile.html')
       
    return render(request, 'project_management/profile.html')
