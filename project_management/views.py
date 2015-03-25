from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from project_management.forms import UserDescriptionForm, ProjectForm
from project_management.models import Project, UserDescription
from django.shortcuts import redirect
from project_management.kris.kris_views import new_task, user_in_project, is_user_privileged
from project_management.kris.kris_models import Task, ProjectInvitation
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date


def index(request):
    return render(request, 'project_management/welcome_page.html')

#returns all the projects which a user owns.
def getUserProjects(user):
    return Project.objects.filter(owner=user)

#returns all the projects which a user is a member of.
def getMemberProjects(user):
    return Project.objects.filter(members=user)

#returns all the projects which a user is admin in.
def getAdminProjects(user):
    return Project.objects.filter(admin=user)


# The dashboard is the user-specific homepage, displaying a menu of all their
# projects on the left sidebar.
@login_required
def dashboard(request):
    return render(request,'project_management/dashboard.html',{})


@login_required
def addProject(request):
    
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


@login_required
def project(request, project_slug):
    project = Project.objects.get(slug=project_slug)

    # Users should not be able to view projects they are not a part
    if not user_in_project(request.user, project):
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
                  {'project': project, 'tasks': tasks, 'new_task_form': new_task_form,
                   'user_project': users_projects,
                   'admin_projects':getAdminProjects(request.user),
                   'member_projects': getMemberProjects(request.user),
                   'user_privileged': is_user_privileged(request.user, project)})


@login_required
# Only visable to project owner - allows project description to be changed.
def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST)

        if form.is_valid():
            project.description = form
            project.save()
            return redirect('/project/{0}'.format(project.slug))

    return render(request,'project_management/project_details.html', {'project':project})


@login_required
# Only visable to the projects owner - deletes the entire project including all it's
# associated tasks from the database.
def end_project(request, project_id):
    project = Project.objects.get(id=project_id)
    #for project_tasks in Task.objects.filter(project=project):
        #project_tasks.delete()
    project.delete()
    return redirect('/dashboard/')


@login_required
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


@login_required
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


@login_required
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


#Button only visable to project owner - removes an admin member from the project.
def remove_admin(request):
    if request.method == "GET":
        user_id= request.GET.get("user_id")
        project_id = request.GET.get("project_id")
    current_project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)
    current_project.admin.remove(user)
    return redirect('/project/{0}'.format(project.slug))


#Button only visable to project owner - removes member from the project.
def remove_member(request):
    if request.method == "GET":
        user_id= request.GET.get("user_id")
        project_id = request.GET.get("project_id")
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)
    project.members.remove(user)
    return redirect('/project/{0}'.format(project.slug))


#Button only visable to project owner - makes member admin of project.
def promote_member(request):
    if request.method == "GET":
        user_id= request.GET.get("user_id")
        project_id = request.GET.get("project_id")
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)
    project.members.remove(user)
    project.admin.add(user)
    return redirect('/project/{0}'.format(project.slug))


#Button only visable to project owner - makes admin regular member of project.
def demote_admin(request):
    if request.method == "GET":
        user_id= request.GET.get("user_id")
        project_id = request.GET.get("project_id")
    project = Project.objects.get(id=project_id)
    user = User.objects.get(id=user_id)
    project.admin.remove(user)
    project.members.add(user)
    return redirect('/project/{0}'.format(project.slug))


@login_required
#User profile allows user to change password and add a short description about themselves.
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
       
    return render(request, 'project_management/profile.html',
                  {'user_project': getUserProjects(request.user),
                   'admin_projects':getAdminProjects(request.user),
                   'member_projects': getMemberProjects(request.user)})
