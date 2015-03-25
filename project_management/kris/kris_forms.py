from django import forms
from project_management.kris.kris_models import Task, Message, File


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'users')
        exclude = ("project",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'description')

class UploadFileForm(forms.Form):
 	title = forms.CharField(max_length = 36, help_text = "Please enter a title")
 	taskFile = forms.FileField()
 	class Meta:
 		model = File
 		fields = ['title', 'taskFile', 'task', 'user']


 		