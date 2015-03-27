from django import forms
from project_management.kris.kris_models import Task, Message, File, GlobalFile


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'users')
        exclude = ("project",)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('title', 'description')

class FileForm(forms.ModelForm):
 	title = forms.CharField(max_length = 64, help_text = "Please enter a title")
 	taskFile = forms.FileField(help_text = "Select a file")
	
 	class Meta:
 		model = File
 		fields = ('title', 'taskFile', 'description',)

class GlobalFileForm(forms.ModelForm):
	title = forms.CharField(max_length = 64, help_text = "Please enter a title")
	projectFile = forms.FileField(help_text = "Select a file")
	class Meta:
		model = GlobalFile
		fields = ('title', 'projectFile', 'description',)
 		