# -*- coding: utf-8 -*-
from django import forms


class SearchBox(forms.Form):
    string = forms.CharField(label='',
        initial='Buscar',
        required=False,
        widget=forms.TextInput(attrs={'class': 'header-seach-form-field'}))
