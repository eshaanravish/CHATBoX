# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Message, IntegerValue, ChatboxUser


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'reciever', 'message', 'created_at')

admin.site.register(Message, MessageAdmin)


class IntegerValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

admin.site.register(IntegerValue, IntegerValueAdmin)



class ChatboxUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

admin.site.register(ChatboxUser, ChatboxUserAdmin)
