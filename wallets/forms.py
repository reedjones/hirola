from django import forms


class ChargeForm(forms.Form):
    price = forms.IntegerField()


