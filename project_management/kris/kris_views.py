from django.shortcuts import render, render_to_response
from project_management.kris.kris_forms import MessageForm
from project_management.kris.kris_forms import TaskForm
from project_management.kris.kris_models import Task, Message
from django.shortcuts import HttpResponse, redirect
from project_management.models import Project

from .kris_forms import UploadFileForm
from somewhere import handle_uploaded_file

import json


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
        # TODO Doesn't add users
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


def task(request, task_id):
    '''View responsible for displaying a particular task.

    TODO validate whether the current user is in this project
    :param request: HTTP request.
    :param task_id: Id of task
    :return: Rendering ot the task
    '''
    task = Task.objects.get(id=task_id)

    # Users should not be able to view tasks of projects they're not members of
    if not (request.user in task.project.members.all() or request.user == task.project.owner):
        return redirect('/dashboard/')
    return render(request, "project_management/task.html", {'task': task})


def complete_task(request):
    '''View responsible for task completion by task members.

    This is used by with a script inside tasks.js.
    :param request: HTTP request.
    :return: Boolean value of whether the task is completed.
    '''

    task = None
    if request.method == "GET":
        task = Task.objects.get(id=request.GET["task_id"])
        task.completed = not task.completed
        task.save()
    return HttpResponse(task.completed)


def approve_task(request, task_id):
    '''Approve task completion.

    TODO: add validation current logged user is authorised to approve tasks.

    :param request:
    :param task_id:
    :return:
    '''
    task = Task.objects.get(id=task_id)
    task.approved = True
    task.save()
    return redirect("/project/{0}".format(task.project.slug))


def completed_and_approved_tasks(request, project_slug):
    '''Display all completed and approved tasks.
    :param request:
    :param project_id Id of current project
    :return:
    '''
    project = Project.objects.get(slug=project_slug)
    tasks = Task.objects.filter(approved=True, project=project)
    return render(request, "project_management/tasks/completed_tasks.html", {'tasks': tasks, 'project': project})


def new_message(request, task_id):
    task = Task.objects.get(id=task_id)
    user = request.user
    print user.id
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

def message(request, message_id):
    message = Message.objects.get(id = message_id)
    user = request.user
    task = request.task
    return render(request, "project_management/message.html", {'message': message})



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


def get_offset_task_json(request):
    page = 0
    response = []
    if request.method == "GET":
        page = request.GET["page"]

    for task in get_offset_tasks(page=page, project=Project.objects.first()):
        task_data = {"title": task.title, "description": task.description}
        response.append(task_data)

    return HttpResponse(json.dumps(response), content_type="application/json")


def get_offset_tasks(page=0, project=None):
    # This part might need to be reworked
    if project is None:
        return Task.objects.all()[page * 4:page * 4 + 4]
    else:
        return Task.objects.filter(project=project, approved=False)[page * 4:page * 4 + 4]

def upload_file(request):
    if request.method = 'POST':
        form - UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['files'])
            return HttpResponseRedirect('/success/url')
        else:
            form = UploadFileForm()
        return render_to_response('upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)