from django.contrib.auth.models import User
from django.db import models


class UserDescription(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length = 200,blank = True)

    def __unicode__(self):
        return self.user.username


class Project(models.Model):
    owner = models.OneToOneField(User)
    name = models.CharField(max_length = 20, unique = True)
    description = models.CharField(max_length = 200, blank = True)
    members = models.ManyToManyField(User, related_name="working_member")

    def __unicode__(self):
        return self.name

##class ProjectMembers(models.Model):
##    project = models.ForeignKey(Project)
##    member = models.ForeignKey(User)
    
