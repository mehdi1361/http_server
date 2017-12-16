# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from base.models import Base, BaseUnit

# from django.db


# Create your models here.


class BenefitBox(Base):
    TYPE = (
        ('GEM', 'gem'),
        ('COIN', 'coin')
    )
    name = models.CharField(_('name'), max_length=40)
    box = models.CharField(_('box'), max_length=4, choices=TYPE)
    quantity = models.PositiveIntegerField(_('quantity'), default=1)
    flag_api = models.BooleanField(_('show box for user'), default=False)

    class Meta:
        verbose_name = _('benefit_box')
        verbose_name_plural = _('benefit_boxes')
        db_table = 'benefit_box'

    def __str__(self):
        return '{}'.format(self.name)


class Unit(BaseUnit, Base):
    image_logo = models.ImageField(_('image'), upload_to='unit/logo')
    image = models.ImageField(_('image'), upload_to='unit/image')

    class Meta:
        verbose_name = _('unit')
        verbose_name_plural = _('units')
        db_table = 'unit'

    def __str__(self):
        return '{}'.format(self.name)


class Hero(BaseUnit, Base):
    name = models.CharField(_('name'), max_length=50, unique=True)
    image_logo = models.ImageField(_('image'), upload_to='hero/logo')
    image = models.ImageField(_('image'), upload_to='hero/image')

    class Meta:
        verbose_name = _('hero')
        verbose_name_plural = _('heroes')
        db_table = 'hero'

    def __str__(self):
        return '{}'.format(self.name)

