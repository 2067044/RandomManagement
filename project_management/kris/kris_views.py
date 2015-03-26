from django.shortcuts import render, render_to_response
from project_management.kris.kris_forms import MessageForm, UploadFileForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from project_management.kris.kris_forms import MessageForm
from project_management.kris.kris_forms import TaskForm
from project_management.kris.kris_models import Task, Message, File
from django.shortcuts import HttpResponse, redirect
from project_management.models import Project

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from django.core.urlresolvers import reverse
from django.template import RequestContext


@login_required
def new_task(request, project_id):
    '''Task is added to the appropriate project.

    POST request adds a new task and redirects to the appropriate project.
    TODO missing form validation...
    :param request HTTP request.
    :param project_id Id of project to which the task is related.
    :return: The task form if the request is not POST
    '''

    project = Project.objects.get(id=project_id)

    if request.method == 'POST':
        form = TaskForm(request.POST)

        # Need to consider validation later
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            task.users.add(*form.cleaned_data['users'])
            task.save()
            return redirect('/project/{0}'.format(project.slug))
        else:
            return redirect('/project/{0}'.format(project.slug))
    else:
        form = TaskForm()

    return form


@login_required
def task(request, task_id):
    '''View responsible for displaying a particular task.

    TODO validate whether the current user is in this project
    :param request: HTTP request.
    :param task_id: Id of task
    :return: Rendering ot the task
    '''
    task = Task.objects.get(id=task_id)
    messages = Message.objects.filter(task=task)
    files = File.objects.filter(task=task)
    msgs_desc = [{'msg': x, 'desc': x.description, 'date': x.date} for x in messages]
    context_dict = {}
    context_dict['task'] = task
    context_dict['messages'] = messages
    context_dict['msgs_desc'] = msgs_desc
    context_dict['files'] = files
    logged_user = request.user
    if not (request.user in task.project.members.all() or request.user == task.project.owner):
        logged_user = request.user
    # Users should not be able to view tasks of projects they're not members of
    if not (logged_user in task.project.members.all() or logged_user == task.project.owner or
                    logged_user in task.project.admin.all()):
        return redirect('/dashboard/')
    return render(request, "project_management/task.html", context_dict)


def message(request, task_id):
    task = Task.objects.get(task=task_id)

    all_messages = Message.objects.filter(task=task)
    paginator = Paginator(all_messages, 4)
    page = request.Get.get('page')

    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        messages = paginator.page(1)
    except EmptyPage:
        messages = paginator.page(paginator.num_pages)

    return render(request, "project_management/message.html", {'messages': messages})


@login_required
def complete_task(request, task_id):
    '''View responsible for task completion by task members.

    This is used by with a script inside tasks.js.
    :param request: HTTP request.
    :return: Boolean value of whether the task is completed.
    '''

    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    # if request.method == "GET":
    # task = Task.objects.get(id=request.GET["task_id"])
    #     task.completed = not task.completed
    #     task.save()
    return redirect("/task/{0}".format(task_id))


@login_required
def approve_task(request, task_id):
    '''Approve task completion.

    TODO: add validation current logged user is authorised to approve tasks.

    :param request:
    :param task_id:
    :return:
    '''
    task = Task.objects.get(id=task_id)
    if not is_user_privileged(request.user, task.project):
        return redirect("/dashboard/")
    task.approved = True
    task.save()
    return redirect("/project/{0}".format(task.project.slug))


@login_required
def completed_and_approved_tasks(request, project_slug):
    '''Display all completed and approved tasks.
    :param request:
    :param project_id Id of current project
    :return:
    '''
    project = Project.objects.get(slug=project_slug)
    if not user_in_project(request.user, project):
        return redirect('/dashboard/')
    tasks = Task.objects.filter(approved=True, project=project)
    return render(request, "project_management/tasks/completed_tasks.html", {'tasks': tasks, 'project': project})


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if not is_user_privileged(request.user, task.project):
        return redirect('/dashboard/')
    task_project = task.project
    task.delete()
    return redirect("/project/{0}".format(task_project.slug))


# ---------Konstantin-----------------------
@login_required
def new_message(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    # print user.id
    if request.method == "POST":
        formM = MessageForm(request.POST)

        if formM.is_valid():
            message = formM.save(commit=False)
            message.task = task
            message.user = user
            message.save()

            return redirect("/task/{0}/".format(task_id))
        else:
            return redirect("/task/{0}/".format(task_id))
    else:
        formM = MessageForm()

    return formM


@login_required
def search_for_tasks(request):
    '''Function returns a json response with all the tasks that contain
    a the expression in a query passed through a GET request.
    :param request:
    :return:
    '''
    response = []
    query = None
    project_id = None
    if request.method == "GET":
        query = request.GET["query"]
        project_id = request.GET["project_id"]
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(title__contains=query, project=project, approved=False)
    for task in tasks:
        response.append({"title": task.title, "description": task.description[:50], "id": task.id})

    return HttpResponse(json.dumps(response), content_type="application/json")


def user_in_project(user, project):
    '''

    :param user:
    :param project:
    :return: True if the user is either the owner, an admin or a member of a project.
    '''
    if user in project.members.all() or user == project.owner or user in project.admin.all():
        return True
    return False


def is_user_privileged(user, project):
    '''

    :param user:
    :param project:
    :return: True if the user is an owner or an admin.
    '''
    if user == project.owner or user in project.admin.all():
        return True
    return False


# def handle_uploaded_file(f):
# with open('some/file/name.txt', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def add_file(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            formF = File(taskFile=request.FILES['taskFile'])
            formF.save()
            formF.task = task
            formF.user = user
            formF.save()
            return redirect("/task/{0}/".format(task_id))
    else:
        form = UploadFileForm()  # A empty, unbound form
    files = File.objects.filter(task=task)
    return render("/task/{0}/".format(task_id), {'files': files})


    # if request.method == "POST":
    #     upload_file = UploadFileForm(request.POST, request.FILES)

    #     if upload_file.is_valid():
    #         upload_file = uploadedFile(taskFile=self.get_form_kwargs().get('files')['taskFile'])
    #         upload_file.task = task
    #         upload_file.user = user
    #         upload_file.save()
    # #         fileForm = fileForm.save(commit=False)
    # #         fileForm.task = task
    # #         fileForm.user = user
    # #         fileForm.save()

    #         return redirect('/task/{0}/'.format(task_id))
    #     else:
    #         return redirect("/task/{0}/".format(task_id))
    # else:
    #     upload_file = UploadFileForm()

    # return upload_file

