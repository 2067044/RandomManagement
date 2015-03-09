from django import forms
from django.contrib.auth.models import User
from project_management.models import UserDescription

#A form so that users can add a description
#to be implemented in a profile / edit_profile page
class UserDescriptionForm(forms.ModelForm):
    class Meta:
        model = UserDescription
        fields = ('description',)
