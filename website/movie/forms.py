from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    accept = forms.BooleanField(error_messages={'required': 'You must accept the policy'}, label="I accept our policy.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
