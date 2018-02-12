from django import forms
from django.utils.translation import ugettext as _

from .models import Order


class OrderCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Order Name',
        max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control m-input', 'placeholder': 'Title'})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control m-input m-textarea', 'placeholder': 'Description'})
    )

    class Meta:
        model = Order
        fields = ('name', 'description',)

