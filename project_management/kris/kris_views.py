from django.shortcuts import render
from django.shortcuts import redirect
from project_management.kris.kris_forms import TaskForm


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
