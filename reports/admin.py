# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db.models import Count, Sum

from reports.models import UserHeroSummary
from .models import Battle, BattleTransaction, TroopReport

from django.contrib.admin import SimpleListFilter


class TransactionInline(admin.TabularInline):
    model = BattleTransaction


@admin.register(Battle)
class BattleAdmin(admin.ModelAdmin):
    list_display = ['player_1', 'player_1_bot', 'player_2', 'player_2_bot', 'status', 'battle_id',
                    'created_date', 'updated_date']
    inlines = [TransactionInline, ]
    list_filter = ['created_date', ]


@admin.register(UserHeroSummary)
class UserHeroSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/user_hero_summary.html'
    date_hierarchy = 'created_date'

    list_filter = (
        'hero',
    )

    def changelist_view(self, request, extra_context=None):
        response = super(UserHeroSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id'),
        }

        response.context_data['summary'] = list(
            qs.filter(enable_hero=True).values('hero__moniker').annotate(**metrics).order_by('-hero')
        )

        return response


@admin.register(TroopReport)
class TroopReportAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['troop', 'win', 'lose']

    list_editable = []
    readonly_fields = ['troop', 'win', 'lose', 'params']