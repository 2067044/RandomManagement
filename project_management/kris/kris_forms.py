from django import forms
from project_management.kris.kris_models import Task, Message, File


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'users', 'fileTask')
        exclude = ("project",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'description')

class UploadFileForm(forms.ModelForm):
	class Meta:
		model = File
		fileTask = forms.FileField( label = "select a file")