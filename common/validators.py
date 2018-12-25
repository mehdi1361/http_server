from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


def validate_percent(value):
    if value > 100:
        raise ValidationError(
            _('%(value)s is not percentage'),
            params={'value': value},
        )


def validate_sequence(value):
    if value > len(settings.CHEST_SEQUENCE):
        raise ValidationError(
            _('%(value)s is not in sequence'),
            params={'value': value},
        )


def validate_unit_spell(value):
    from objects.models import UnitSpell

    if not UnitSpell.objects.filter(pk=value).exists():
        raise ValidationError(
            _('%(value)s is not spell id'),
            params={'value': value},
        )


def validate_hero_spell(value):
    from objects.models import HeroSpell

    if not HeroSpell.objects.filter(pk=value).exists():
        raise ValidationError(
            _('%(value)s is not spell id'),
            params={'value': value},
        )


def validate_chakra_spell(value):
    from objects.models import ChakraSpell

    if not ChakraSpell.objects.filter(pk=value).exists():
        raise ValidationError(
            _('%(value)s is not spell id'),
            params={'value': value},
        )