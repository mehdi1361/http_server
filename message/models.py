# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords

# Create your models here.


class NewsLetter(Base):
    subject = models.CharField(_('subject'), max_length=500)
    body = models.TextField(_('body'))
    expire_date = models.DateTimeField(_('expire date'))

    history = HistoricalRecords()


    class Meta:
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletter')
        db_table = 'newsletter'

    def __str__(self):
        return '{}'.format(self.subject)


class Inbox(Base):
    TYPE = (
        ('UNREAD', 'unread'),
        ('READ', 'read'),
        ('EXPIRED', 'expire')
    )

    message_type = models.CharField(_('message type'), max_length=20, choices=TYPE, default='unread', db_index=True)
    news = models.ForeignKey(NewsLetter, verbose_name=_('news'), related_name='inbox')
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='inbox')

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('inbox')
        verbose_name_plural = _('inbox')
        db_table = 'inbox'

    def __str__(self):
        return '{}'.format(self.message_type)