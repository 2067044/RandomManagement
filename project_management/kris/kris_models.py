from django.db import models
from django.contrib.auth.models import User
from project_management.models import Project
from time import time


class Task(models.Model):
    title = models.CharField(unique=True, max_length=40)
    completed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    description = models.TextField(max_length=1000)
    due_date = models.DateField()
    app_label = 'project_management'
    users = models.ManyToManyField(User)
    project = models.ForeignKey(Project, default=None)

    def __unicode__(self):
        return self.title

    class Meta:
        # Show the most urgent tasks on top
        ordering = ('due_date',)


class ProjectInvitation(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return "User: {0}, Project: {1}".format(self.user, self.project)


class DummyProject(models.Model):
    title = models.CharField(max_length=20)

    def __unicode__(self):
        return self.title


class Message(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    user = models.ForeignKey(User)
    task = models.ForeignKey(Task)
    date = models.DateField(auto_now_add=True)  # to be changed to DateTimeField

    def __unicode__(self):
        return self.title


def filePath(self, filename):
    url = "uploads/%s/%s/%s" % (self.task.title, self.user.username, filename)
    return url


######## Model for files in tasks
class File(models.Model):
    title = models.CharField(max_length=20)
    taskFile = models.FileField(upload_to=filePath)
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=1000)

    def __unicode__(self):
        return self.title


def filePathGlobal(self, filename):
    url = "uploads/%s/%s/%s" % (self.project.name, self.user.username, filename)
    return url


class GlobalFile(models.Model):
    title = models.CharField(max_length=20)
    projectFile = models.FileField(upload_to=filePathGlobal)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length = 1000)

    def __unicode__(self):
        return self.title