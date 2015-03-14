import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RandomManagement.settings')

import django
django.setup()

from project_management.kris.kris_models import Task
from project_management.models import Project
from django.contrib.auth.models import User
from datetime import date


def populate():
    user1 = add_user("test1", "pass", "p@p.com")
    user2 = add_user("test2", "pass", "p@p.com")
    user3 = add_user("test3", "pass", "p@p.com")
    user4 = add_user("test4", "pass", "p@p.com")

    project1 = add_project(user1, "First project", "First project description", [user2, user3, user4])

    add_task("Task1", "Some task description", date(2015, 2, 15), [user1, user2], project1, True)
    add_task("Task2", "Some task description", date(2015, 2, 12), [user3], project1)
    add_task("Task3", "Some task description", date(2015, 2, 11), [user4, user2], project1)
    add_task("Task4", "Some task description", date(2015, 3, 15), [user1], project1)


def add_user(username, password, email):
    '''
    Creates a new user
    '''
    u = User.objects.get_or_create(username=username)
    u = u[0]
    u.password = password
    u.email = email
    u.save()
    return u


def add_task(title, description, due_date, users, project, completed=False):
    '''
    Creates a new task which has several users responsible for it.
    The 'users' param should be a list
    '''
    t = Task.objects.get_or_create(title=title, defaults={'due_date': date(2015, 1, 1),
                                                          "project": Project.objects.first()},
                                   )
    t = t[0]
    t.description = description
    t.due_date = due_date
    t.project = project
    t.completed = completed
    t.users.add(*users)
    t.save()
    return t


def add_project(owner, name, description, members):
    '''
    Adds a new project to the test database
    '''
    p = Project.objects.get_or_create(name=name, defaults={'owner': User.objects.first()})
    p = p[0]
    p.owner = owner
    p.description = description
    p.members.add(*members)
    p.save()
    return p


# Start population
if __name__ == '__main__':
    print 'Starting rango population script...'
    populate()
    print 'Population complete.'