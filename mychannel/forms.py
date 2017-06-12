from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from mychannel.models import IntegerValue, Message


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder':'Email-Id'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder':'FirstName'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder':'LastName'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder':'Password'})

