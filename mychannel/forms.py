from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from mychannel.models import IntegerValue, Message, ChatboxUser


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


class ChatboxUserForm(ModelForm):
    picture = forms.ImageField(label='Select a file', help_text='max. 42 megabytes')

    class Meta:
        model = ChatboxUser
        fields = ('picture', 'bio')


    def __init__(self, *args, **kwargs):
        super(ChatboxUserForm, self).__init__(*args, **kwargs)
        self.fields['picture'].widget.attrs.update({'class': 'form-control'})
        self.fields['bio'].widget.attrs.update({'class': 'form-control', 'placeholder':'Bio'})
