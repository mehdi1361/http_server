# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


@python_2_unicode_compatible
class ShoppingGemLog(Base):
    SHOPPING_TYPE = (
        ('gem', 'gem'),
        ('coin', 'coin'),
        ('chest', 'chest'),
        ('offer', 'offer'),
    )

    amount = models.PositiveIntegerField(_('amount'))
    price = models.PositiveIntegerField(_('price'))
    shopping_type = models.CharField(_('shopping type'), max_length=50, choices=SHOPPING_TYPE, default='gem')
    player = models.ForeignKey(User, verbose_name=_('player'))

    class Meta:
        verbose_name = _('shopping_log')
        verbose_name_plural = _('shopping_logs')
        db_table = 'shopping_logs'

    def __str__(self):
        return '{}'.format(self.name)