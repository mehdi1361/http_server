# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CTM, CTMUnit, CTMHero, BotMatchMaking


class CTMUnitInline(admin.StackedInline):
    model = CTMUnit


class CTMHeroInline(admin.StackedInline):
    model = CTMHero


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
        'card_try',
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
        'card_try'
    ]

    inlines = (CTMUnitInline, CTMHeroInline)


@admin.register(BotMatchMaking)
class BotMatchMakingAdmin(admin.ModelAdmin):
    list_display = [
        'strike_number',
        'bot_ai',
        'min_level',
        'max_level',
        'step_forward',
        'step_backward'
    ]
    list_editable = [
        'bot_ai',
        'min_level',
        'max_level',
        'step_forward',
        'step_backward'
    ]
