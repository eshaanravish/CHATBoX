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
from django.db.models import Q
from django.contrib.auth.models import User

from mychannel.models import Message

from mychannel.forms import UserForm
# Create your views here.

def homepage(request):
    if request.method == "POST":
        users = User.objects.all()
        form = UserForm(request.POST, use_required_attribute= False)
        if form.is_valid():
            username = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                pass
            else:
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )
            user = authenticate(username=username, password=password)
            login(request, user)
            users = []
            all_users = User.objects.all()
            for i in all_users:
                if i == request.user:
                    continue
                elif i == User.objects.get(is_superuser=True):
                    continue
                else:
                    users.append(i)
            messages = Message.objects.all().order_by("created_at")
            if messages[0].sender == user:
                friend_id = messages[0].reciever.id
            else:
                friend_id = messages[0].sender.id

            return redirect('dashboard', user_id=friend_id)
        else:
            error_message = "Please fill the valid details."
            return render(request, 'mychannel/home.html', {'form': form, 'error_message': error_message})
    else:
        error_message = ""
        form = UserForm(request.POST, use_required_attribute= False)
        return render(request, 'mychannel/home.html', {'form':form})

@login_required(login_url="/login/")
def dashboard(request, user_id):
    users = []
    all_users = User.objects.all()
    for i in all_users:
        if i == request.user:
            continue
        elif i == User.objects.get(is_superuser=True):
            continue
        else:
            users.append(i)
    friend = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        Q (sender=request.user, reciever=friend) |
        Q (sender=friend, reciever=request.user)).order_by("created_at")
    return render(request, 'mychannel/dashboard.html', {'user': request.user, 'friend_top': friend, 'users': users, 'messages': messages})


@login_required(login_url="/login/")
def msg_sent(request):
    if request.is_ajax():
        login_user = request.user
        user_id = request.GET.get("user_id", "")
        message = request.GET.get("message", "")
        user = User.objects.get(id=user_id)
        msg = Message.objects.create(
            sender=login_user,
            reciever=user,
            message=message,
        )
        created = msg.created_at.isoformat()
        response = {'status': True, 'data': created}
        return HttpResponse(json.dumps(response))
    else:
        return Http404


@login_required(login_url="/login/")
def fetch_user(request):
    if request.is_ajax():
        login_user = request.user
        user_id = request.GET.get("user_id", "")
        user = User.objects.get(pk=user_id)
        messages = Message.objects.filter(
            Q (sender=login_user, reciever=user) |
            Q (sender=user, reciever=login_user)).order_by("created_at")
        all_messages = []
        for msg in messages:
            message = []
            message.append(msg.sender.first_name)
            message.append(msg.sender.first_name[0])
            message.append(msg.reciever.first_name)
            message.append(msg.message)
            message.append(msg.created_at.isoformat())
            all_messages.append(message)
        response = {'status': True, 'data': all_messages}
        return HttpResponse(json.dumps(response))
    else:
        return Http404
    


@login_required(login_url="/login/")
def dashboard_global(request):
    login_user = request.user
    users = []
    all_users = User.objects.all()
    for i in all_users:
        if i == request.user:
            continue
        elif i == User.objects.get(is_superuser=True):
            continue
        else:
            users.append(i)
    friend = users[0]
    messages = Message.objects.filter(
        Q (sender=login_user, reciever=friend) |
        Q (sender=friend, reciever=login_user)).order_by("created_at")
    return render(request, 'mychannel/dashboard_global.html', {'user': login_user, 'friend_top': friend, 'users': users, 'messages': messages})



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
            first_name = user.first_name
            last_name = user.last_name
            response = {'status': True, 'firstname': first_name, 'lastname': last_name}
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