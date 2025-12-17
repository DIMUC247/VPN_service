from django import forms

from .models import Subscription


class SubForm(forms.Form):
    sub = forms.ModelChoiceField(
        queryset=Subscription.objects.all(),
        label='Оберіть підписку',
        widget=forms.Select(attrs={'class':'form-control'}),
        empty_label="Оберіть підписку"
    )

