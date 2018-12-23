from django import forms
from objects.models import League, UserCurrency


COUNT_STATUS = (
    (1, '1'),
    (2, '2'),
    (5, '5'),
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
    ('M', 'magical'),
)

LEAGUE = ((item.id, item.league_name) for item in League.league_real.all())
PLAYERS = ((player.user_id, player.name) for player in UserCurrency.objects.all())


class CtmTestForm(forms.Form):
    count = forms.ChoiceField(choices=COUNT_STATUS)
    chest = forms.ChoiceField(choices=CHEST_STATUS)
    league = forms.ChoiceField(choices=LEAGUE)
    player = forms.ChoiceField(choices=PLAYERS)

    # def __init__(self, *args, **kwargs):
    #     super(CtmTestForm, self).__init__(*args, **kwargs)
    #     self.fields['player'].queryset = UserCurrency.objects.all()
