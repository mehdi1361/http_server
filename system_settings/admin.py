# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CTM


@admin.register(CTM)
class CTMAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'chest_type',
        'league',
        'min_coin',
        'max_coin',
        'min_gem',
        'max_gem',
        'min_troop',
        'max_troop',
        'chance_troop',
        'min_hero',
        'max_hero',
        'chance_hero',
        'total',
    ]
    list_editable = [
        'chest_type',
        'league',
        'min_coin',
        'max_coin',
        'min_gem',
        'max_gem',
        'min_troop',
        'max_troop',
        'chance_troop',
        'min_hero',
        'max_hero',
        'chance_hero',
        'total',
    ]
