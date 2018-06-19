# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Battle, BattleTransaction


class TransactionInline(admin.TabularInline):
    model = BattleTransaction


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ['player_1', 'player_1_bot', 'player_2', 'player_2_bot', 'status', 'battle_id',
                    'created_date', 'updated_date']
    inlines = [TransactionInline, ]

<<<<<<< HEAD
    list_filter = ['created_date', ]

=======
>>>>>>> 9c918644d14535bc8ac1b7e461cd7eb4fef0eb95
