# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Store(Base):
    name = models.CharField(_('store name'), max_length=50)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')
        db_table = 'stores'

    def __str__(self):
        return '{}'.format(self.name)


class EnableShop(models.Manager):
    def get_queryset(self):
        return super(Shop, self).get_queryset().exclude(enable=True)


@python_2_unicode_compatible
class Shop(Base):
    name = models.CharField(_('shop name'), max_length=50)
    coins = JSONField(_('coins'))
    gems = JSONField(_('gems'))
    chests = JSONField(_('chests'))
    special_offer = JSONField(_('special offer'), null=True, default=None, blank=True)
    store = models.ForeignKey(Store, verbose_name=_('store'))
    enable = models.BooleanField(_('enable shop item'), default=False)

    objects = models.Manager()
    enable_shop = EnableShop()

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        db_table = 'shops'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class PurchaseLog(Base):
    user = models.ForeignKey(User, verbose_name=_('user purchase'), related_name='purchases')
    store_purchase_token = models.CharField(_('store purchase token'), max_length=50)

    def __str__(self):
        return "{}".format(self.user.username)
