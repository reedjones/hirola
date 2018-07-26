from django import forms
from services.models import ServiceInspector


class InspectorForm(forms.Form):
    note = forms.CharField(widget=forms.Textarea)
    reason = forms.ChoiceField(choices=ServiceInspector.reason_choices)
