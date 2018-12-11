# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CTM, BotMatchMaking, CustomBot, CustomBotTroop, CustomToken


@admin.register(CTM)
class CTMAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'chest_type',
        'league',
        'is_must_have_hero',
        'is_must_have_spell',
        'is_must_have_troop'
    ]

    fieldsets = (
        ('main', {
            'classes': ('collapse',),
            'fields': (
                'chest_type',
                'league',
                'total',
                'card_try',
                'params'
            )
        }),
        ('general chance', {
            'classes': ('collapse',),
            'fields': (
                'min_coin',
                'max_coin',
                'min_gem',
                'max_gem',
            )
        }),
        ('epic chance', {
            'classes': ('collapse',),
            'fields': (
                'epic_chance',
                'min_epic',
                'max_epic'
            )
        }),
        ('rare chance', {
            'classes': ('collapse',),
            'fields': (
                'rare_chance',
                'min_rare',
                'max_rare'
            )
        }),
        ('must have', {
            'classes': ('collapse',),
            'fields': (
                'is_must_have_hero',
                'must_have_hero_type',
                'min_have_hero',
                'max_have_hero',
                'must_have_hero',
                'is_must_have_spell',
                'must_have_spell_type',
                'min_have_spell',
                'max_have_spell',
                'must_have_spell',
                'is_must_have_troop',
                'must_have_troop_type',
                'min_have_troop',
                'max_have_troop',
                'must_have_troop'
            )
        }),
    )

    # inlines = (CTMUnitInline, CTMHeroInline)


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


class CustomBotTroopAdmin(admin.StackedInline):
    model = CustomBotTroop


@admin.register(CustomBot)
class CustomBotAdmin(admin.ModelAdmin):
    list_display = ['bot_name', 'enable', 'troops', 'hero', 'level']
    list_editable = ['enable', 'hero', 'level']
    inlines = [CustomBotTroopAdmin, ]

    def troops(self, bot):
        lst_troops = []

        for troop in bot.troops.all():
            lst_troops.append(troop.troop.moniker)

        return ', '.join(lst_troops)


@admin.register(CustomToken)
class CustomTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token_desc', 'gem_reward', 'coin_reward', 'token', 'expire_date', 'enable']
    list_editable = ['token_desc', 'gem_reward', 'coin_reward', 'expire_date', 'enable']
    readonly_fields = ['token', 'expire_date', 'enable']