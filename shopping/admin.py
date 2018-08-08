# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Store, Shop, PurchaseLog, CurrencyLog


class ShopInline(admin.StackedInline):
    model = Shop


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')
    inlines = (ShopInline, )


@admin.register(PurchaseLog)
class PurchaseLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'store_purchase_token',
        'params',
        'store_params',
        'created_date',
        'updated_date',
        'shop'
    )


@admin.register(CurrencyLog)
class CurrencyLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'quantity_used', 'type_buy', 'quantity_buy', 'created_date', 'updated_date')