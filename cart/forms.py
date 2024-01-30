from django.db.models import fields
from .models.carts import Cart

from django import forms
from django.forms.models import BaseInlineFormSet


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'