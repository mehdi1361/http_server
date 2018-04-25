# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from .models import Inbox, NewsLetter


@admin.register(NewsLetter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'body', 'created_date', 'updated_date', 'expire_date')
    search_fields = ('subject', )


@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'message_type', 'created_date', 'updated_date')
