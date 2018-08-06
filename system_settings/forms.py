from django import forms


class CtmTestForm(forms.Form):
    count = forms.ChoiceField(choices=[10, 20, 50, 100, 200, 500, 100])
