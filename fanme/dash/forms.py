# -*- coding: utf-8 -*-
from django import forms


class SearchBox(forms.Form):
    string = forms.CharField(label='',
        initial='Buscar',
        required=False,
        #~ error_messages={'required': 'Es necesario un Nombre'},
        widget=forms.TextInput(attrs={'class': 'header-seach-form-field'}))
