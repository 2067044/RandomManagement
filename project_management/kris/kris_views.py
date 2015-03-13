from django.shortcuts import render
from django.shortcuts import redirect
from project_management.kris.kris_forms import TaskForm
from project_management.kris.kris_models import Task


def new_task(request):
    '''
    ' New task generation. TODO missing form validation :)
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = TaskForm(request.POST)

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
