from django.shortcuts import render
from project_management.kris.kris_forms import MessageForm
from project_management.kris.kris_forms import TaskForm
from project_management.kris.kris_models import Task
from django.shortcuts import HttpResponse, redirect
from project_management.models import Project

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
    logged_user = request.user
    # Users should not be able to view tasks of projects they're not members of
    if not (logged_user in task.project.members.all() or logged_user == task.project.owner or
             logged_user in task.project.admin.all()):
        return redirect('/dashboard/')
    return render(request, "project_management/task.html", {'task': task})


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
    #     task = Task.objects.get(id=request.GET["task_id"])
    #     task.completed = not task.completed
    #     task.save()
    return redirect("/task/{0}".format(task_id))


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


def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if not is_user_privileged(request.user, task.project):
        return redirect('/dashboard/')
    task_project = task.project
    task.delete()
    return redirect("/project/{0}".format(task_project.slug))

# ---------Konstantin-----------------------
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


