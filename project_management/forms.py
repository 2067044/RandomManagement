from django import forms
from django.contrib.auth.models import User
from project_management.models import UserDescription, Project

# A form so that users can add a description
# to be implemented in a profile / edit_profile page
class UserDescriptionForm(forms.ModelForm):
    class Meta:
        model = UserDescription
        fields = ('description',)

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','description',)

##class Add_User(forms.ModelForm):
##    class Meta:
##        model = Membership
##        fields = ('member',)
