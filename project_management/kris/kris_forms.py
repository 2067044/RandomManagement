from django import forms
from project_management.kris.kris_models import Task, Message


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'users',)
        exclude = ("project",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'description')

