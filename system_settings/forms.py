from django import forms
from objects.models import League


COUNT_STATUS = (
    (10, '10'),
    (20, '20'),
    (50, '50'),
    (100, '100'),
    (200, '200'),
    (500, '500'),
    (1000, '1000'),
)

CHEST_STATUS = (
    ('W', 'wooden'),
    ('S', 'silver'),
    ('G', 'gold'),
    ('C', 'crystal'),
)

LEAGUE = ((item.id, item.league_name) for item in League.league_real.all())


class CtmTestForm(forms.Form):
    count = forms.ChoiceField(choices=COUNT_STATUS)
    chest = forms.ChoiceField(choices=CHEST_STATUS)
    league = forms.ChoiceField(choices=LEAGUE)
