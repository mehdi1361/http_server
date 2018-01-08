# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Store(Base):
    name = models.CharField(_('store name'), max_length=50)

    class Meta:
        verbose_name = _('store')
        verbose_name_plural = _('stores')
        db_table = 'stores'

    def __str__(self):
        return '{}'.format(self.name)


@python_2_unicode_compatible
class Shop(Base):
    name = models.CharField(_('shop name'), max_length=50)
    coins = JSONField(_('coins'))
    gems = JSONField(_('gems'))
    chests = JSONField(_('chests'))
    special_offer = JSONField(_('special offer'), null=True, default=None)
    store = models.ForeignKey(Store, verbose_name=_('store'))
    enable = models.BooleanField(_('enable shop item'), default=True)

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')
        db_table = 'shops'

    def __str__(self):
        return '{}'.format(self.name)
