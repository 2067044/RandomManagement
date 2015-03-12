from django.contrib.auth.models import User

from project_management.kris.kris_models import *


class UserDescription(models.Model):
    user = models.OneToOneField(User)
    description = models.CharField(max_length = 200)

    def __unicode__(self):
        return self.user.username

