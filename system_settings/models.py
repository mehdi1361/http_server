# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from objects.models import League
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class CTM(Base):
    CHEST_TYPE = (
        ('W', 'wooden'),
        ('S', 'silver'),
        ('G', 'gold'),
        ('C', 'crystal'),
    )

    chest_type = models.CharField(_('chest type'), max_length=50, default='W', choices=CHEST_TYPE)
    league = models.ForeignKey(League, verbose_name=_('league'), related_name='ctm_chests')
