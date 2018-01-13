# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Store, Shop


class ShopInline(admin.StackedInline):
    model = Shop


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')
    inlines = (ShopInline, )