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
 	class Meta:
 		model = File
 		fields = ('title')
 		taskFileField = forms.FileField( label = "select a file", help_text='max. 5 megabytes')