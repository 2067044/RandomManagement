from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from project_management.forms import UserDescriptionForm, ProjectForm
from project_management.models import Project, UserDescription
from django.shortcuts import redirect
from project_management.kris.kris_views import new_task
from project_management.kris.kris_models import Task, ProjectInvitation
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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

# def project(request, project_slug):
#     project = Project.objects.get(slug=project_slug)
#
#
#     if request.method == 'POST':
#         print 'TEST 1'
#         member_username = request.POST['add_user']
#         print request.POST['add_user']
#         if member_username.is_valid():
#             new_member = User.objects.filter(username=member_username)
#             project.members.add(new_member)
#             project.save()
#
#     return render(request,'project_management/project.html',{'project':project, 'user_project':users_projects})
#
#     # This determines which css style will be used in the template
#     # Tasks which are more than 9 days due are alright; 4 to 9 is kinda bad;
#     # less than 3 is critical
#     # format: task: [{task:task, colouring:css}]
#     tasks_and_colouring = []
#     current_date = date.today()


def project(request, project_slug):
    project = Project.objects.get(slug=project_slug)

    # Users should not be able to view projects they are not a part
    # of (admins should be included here when they're implemented)
    if not (request.user in project.members.all() or request.user == project.owner):
        return redirect('/dashboard/')

    users_projects = getUserProjects(request.user)

    all_tasks = Task.objects.filter(project=project, approved=False)
    paginator = Paginator(all_tasks, 4)
    page = request.GET.get('page')


    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tasks = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tasks = paginator.page(paginator.num_pages)

    current_date = date.today()

    # Object responsible for handling the creation of new tasks
    new_task_form = new_task(request, project.id)

    # Decide how each task is going to be coloured

    for task in tasks:
        if (task.due_date - current_date).days >= 10:
            task.colouring = 'task-panel-normal-colour'
        elif 3 < (task.due_date - current_date).days < 10:
            task.colouring = 'task-panel-attention-colour'
        else:
            task.colouring = 'task-panel-critical-colour'

    return render(request, 'project_management/project.html',
                  {'project': project, 'tasks': tasks, 'new_task_form': new_task_form, 'user_project': users_projects})


def accept_invitation(request, project_invitation_id):
    '''Function responsible for adding a user to a project.

    :param request:
    :param project_invitation_id Id of the project invitation sent to this user.
    :return:
    '''
    project_invitation = ProjectInvitation.objects.get(id=project_invitation_id)
    user = project_invitation.user
    project = project_invitation.project

    project.members.add(user)
    project_invitation.delete()

    return redirect('/project/{0}'.format(project.slug))


def decline_invitation(request, project_invitation_id):
    '''Function responsible for declining a project invitation.

    :param request:
    :param project_invitation_id:
    :return:
    '''
    project_invitation = ProjectInvitation.objects.get(id=project_invitation_id)
    project_invitation.delete()
    # Refreshes the current page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def send_invitation(request):
    '''Function responsible for generating an invitation. Used inside logged_in.js.

    :param request:
    :return: Either a success message or an appropriate failure message, if the operation cannot be performed
    '''
    if request.method == "GET":
        username = request.GET.get("username")
        project_id = request.GET.get("project_id")

    # Get user, send failure code if username is invalid
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse("No such user.")

    # Whether this particular invitation already exists, send failure code if it does
    project = Project.objects.get(id=project_id)
    if ProjectInvitation.objects.filter(user=user, project=project).exists():
        return HttpResponse("You have already sent an invitation to this user.")

    # If the user is a member of the project return a failure code
    if user in project.members.all():
        return HttpResponse("This user is a member of the project.")

    # Generate an invitation of everything is alright
    project_invitation = ProjectInvitation(user=user, project=project)
    project_invitation.save()

    return HttpResponse("Invitation sent.")


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
