from django.contrib import admin

from project_management.models import UserDescription, Project
from project_management.kris.kris_models import Task, Message, ProjectInvitation, File

admin.site.register(UserDescription)
admin.site.register(Task)
admin.site.register(Project)
admin.site.register(Message)
admin.site.register(ProjectInvitation)
admin.site.register(File)
