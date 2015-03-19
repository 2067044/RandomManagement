from django.shortcuts import render
from project_management.kris.kris_forms import TaskForm
from project_management.kris.kris_models import Task
from django.shortcuts import HttpResponse, redirect
from project_management.models import Project
from django.contrib.auth.models import User
from django.core.paginator import Paginator, InvalidPage, EmptyPage
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
            return redirect('/project/{0}'.format(project_id))
        else:
            return redirect('/project/{0}'.format(project_id))
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
    return redirect("/project/{0}".format(task.project.id))


def completed_and_approved_tasks(request, project_id):
    '''Display all completed and approved tasks.
    :param request:
    :param project_id Id of current project
    :return:
    '''
    project = Project.objects.get(id=project_id)
    tasks = Task.objects.filter(approved=True, project=project)
    return render(request, "project_management/tasks/completed_tasks.html", {'tasks': tasks, 'project': project})


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
        return Task.objects.all()[page*4:page*4+4]
    else:
        return Task.objects.filter(project=project, approved=False)[page*4:page*4+4]
