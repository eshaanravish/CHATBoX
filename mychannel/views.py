# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import json

from django.urls import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, \
redirect, render_to_response, reverse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from django.contrib.auth.models import User

from mychannel.models import Message

from mychannel.forms import UserForm
# Create your views here.

def homepage(request):
    if request.method == "POST":
        users = User.objects.all()
        form = UserForm(request.POST, use_required_attribute= False)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                user = User.objects.get(username=form.cleaned_data['email'])
                login(request, user)
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )
                login(request, user)
                return render(request, 'mychannel/dashboard.html', {'users': users})
        else:
            error_message = "Please fill the valid details."
            return render(request, 'mychannel/dashboard.html', {'form': form, 'error_message': error_message})
    else:
        error_message = ""
        form = UserForm(request.POST, use_required_attribute= False)
        return render(request, 'mychannel/home.html', {'form':form})

@login_required(login_url="/login/")
def dashboard(request):
    login_user = request.user.id
    messages = Message.objects.all().order_by('-created_at')
    users = []
    all_users = User.objects.all()
    for i in all_users:
        if i == request.user:
            continue
        elif i == User.objects.get(is_superuser=True):
            continue
        else:
            users.append(i)
    msg_sender = messages[0].sender
    return render(request, 'mychannel/dashboard.html', {'users': users, 'messages': messages, 'sender': msg_sender })

@login_required(login_url="/login/")
def chatter(request, user_id):
    if request.is_ajax():
        login_user = request.user
        messages = Message.objects.filter(sender=login_user, reciever=user_id)
        message_content = {'messages': messages}
        for item in message_content:
            item['messages'] = model_to_dict(item['messages'])
        response = {'status': True, 'data': message_content}
        return HttpResponse(json.dumps(response))
    else:
        Http404


def user_check(request):
    if request.is_ajax():
        email = request.GET.get('email', '')
        if User.objects.filter(username=email).exists():
            user = User.objects.get(username=email)
            response = {'status': True}
            return HttpResponse(json.dumps(response))
        else:
            response = {'status': False}
            return HttpResponse(json.dumps(response))
    else:
        Http404

@login_required(login_url="/login/")
def userlogout(request):
    logout(request)
    return redirect('/')