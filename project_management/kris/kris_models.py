from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(unique=True, max_length=40)
    completed = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    description = models.TextField(max_length=1000)
    due_date = models.DateField()
    app_label = 'project_management'
    users = models.ManyToManyField(User)

    def __unicode__(self):
        return self.title

    class Meta:
        # Show the most urgent tasks on top
        ordering = ('due_date',)


class DummyProject(models.Model):
    title = models.CharField(max_length=20)

    def __unicode__(self):
        return self.title



