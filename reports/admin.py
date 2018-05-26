# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import Battle, BattleTransaction


class TransactionInline(admin.TabularInline):
    model = BattleTransaction


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ['player_1', 'player_1_bot', 'player_2', 'player_2_bot', 'status', 'battle_id',
                    'created_date', 'updated_date']
    inlines = [TransactionInline, ]