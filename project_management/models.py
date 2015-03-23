from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class UserDescription(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length = 200,blank = True)

    def __unicode__(self):
        return self.user.username


class Project(models.Model):
    owner = models.ForeignKey(User, related_name="owner",unique=False)
    name = models.CharField(max_length = 20, unique = True)
    description = models.CharField(max_length = 200, blank = True)
    members = models.ManyToManyField(User, related_name="working_member", blank=True)
    admin = models.ManyToManyField(User, related_name="Project_admin",blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
    def __unicode__(self):
        return self.name
