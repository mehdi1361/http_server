# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from base.models import Base
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from simple_history.models import HistoricalRecords
from django.db.models import signals


class NewsLetter(Base):
    subject = models.CharField(_('subject'), max_length=500)
    body = models.TextField(_('body'))
    expire_date = models.DateTimeField(_('expire date'))

    history = HistoricalRecords()

    class Meta:
        verbose_name = _('newsletter')
        verbose_name_plural = _('newsletter')
        db_table = 'newsletter'

    def __unicode__(self):
        return unicode('{}'.format(self.subject))


class InboxManager(models.Manager):
    def get_queryset(self):
        return super(InboxManager, self).get_queryset().exclude(message_type='expired').order_by('-id')


class Inbox(Base):
    TYPE = (
        ('UNREAD', 'unread'),
        ('READ', 'read'),
        ('EXPIRED', 'expired')
    )

    message_type = models.CharField(_('message type'), max_length=20, choices=TYPE, default='unread', db_index=True)
    news = models.ForeignKey(NewsLetter, verbose_name=_('news'), related_name='inbox')
    user = models.ForeignKey(User, verbose_name=_('user'), related_name='inbox')

    history = HistoricalRecords()

    objects = models.Manager()
    user_inbox = InboxManager()

    class Meta:
        verbose_name = _('inbox')
        verbose_name_plural = _('inbox')
        db_table = 'inbox'

    def __unicode__(self):
        return unicode('{}'.format(self.message_type))


def create_inbox(sender, instance, created, **kwargs):
    if created:
        for user in User.objects.all():
            Inbox.objects.create(user=user, news=instance)


signals.post_save.connect(create_inbox, sender=NewsLetter)