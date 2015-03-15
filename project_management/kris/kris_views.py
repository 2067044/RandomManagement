from django.shortcuts import render
from django.shortcuts import redirect
from project_management.kris.kris_forms import TaskForm
from project_management.kris.kris_models import Task
from django.shortcuts import HttpResponse, redirect
import json


def new_task(request):
    '''
    ' New task generation. TODO missing form validation :)
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = TaskForm(request.POST)

        # Need to consider validation later
        if form.is_valid():
            form.save(commit=True)
            return redirect('/dashboard/')
        else:
            return redirect("/dashboard/")
    else:
        form = TaskForm()

    return form


def task(request, task_id):
    task = Task.objects.get(id=task_id)
    # validate whether the current user is in this project

    return render(request, "project_management/task.html", {'task': task})


def complete_task(request):
    task = None
    if request.method == "GET":
        task = Task.objects.get(id=request.GET["task_id"])
        task.completed = not task.completed
        task.save()
    return HttpResponse(task.completed)


def approve_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.approved = True
    task.save()
    return redirect("/dashboard/")


def completed_and_approved_tasks(request):
    tasks = Task.objects.filter(approved=True)
    return render(request, "project_management/tasks/completed_tasks.html", {'tasks': tasks})


def get_offset_task_json(request):
    page = 0
    response = []
    if request.method == "GET":
        page = request.GET["page"]

    for task in get_offset_tasks(page):
        response.append(task.__dict__)

    print response
    return HttpResponse(json.dumps(response), content_type="application/json")


def get_offset_tasks(page=0):
    return Task.objects.all()[page*4:page*4+4]