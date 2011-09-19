# -*- coding: utf-8 -*-
from django import forms


class SearchBox(forms.Form):
    string = forms.CharField(label='',
        initial='Buscar',
        required=False,
        widget=forms.TextInput(attrs={'class': 'header-seach-form-field'}))

    def clean_string(self):
        string = self.cleaned_data['string']
        if string == "":
            raise forms.ValidationError("Debe ingresar una palabra")
        return string
