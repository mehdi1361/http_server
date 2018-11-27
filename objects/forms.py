from django import forms
from .models import UnitSpell
from prettyjson import PrettyJSONWidget


class UnitSpellForm(forms.ModelForm):
    class Meta:
        model = UnitSpell
        fields = '__all__'
        widgets = {
            'params': PrettyJSONWidget(),
        }
