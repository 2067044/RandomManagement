from django.contrib import admin

from project_management.models import UserDescription
from project_management.kris.kris_models import Task

admin.site.register(UserDescription)
admin.site.register(Task)

