# -*- coding: utf-8 -*-
from django import forms
#from django.contrib.auth import authenticate
from fanme.items.models import Marca
from fanme.segmentation.models import Topico


class ItemRegisterForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        initial='Nombre',
        required=True,
        error_messages={'required': 'Es necesario un Nombre'},
        widget=forms.TextInput(attrs={'class': 'item-register-name-field'}))
    descripcion = forms.CharField(
        label='Descripción',
        initial='Descripción',
        required=True,
        error_messages={'required': 'Es necesario una descripción'},
        widget=forms.TextInput(attrs={'class': 'item-register-name-field'}))
    topico = forms.ModelChoiceField(
        label='',
        empty_label="Tópico",
        queryset=Topico.objects.all(),
        error_messages={'required': 'Es necesario un Tópico',
            'invalid_choice': 'Opcion no valida'},
        widget=forms.Select(attrs={'class': 'accounts-register-form-field'}))
#    marca = forms.ModelChoiceField(
#        label='',
#        empty_label="Marca",
#        queryset=Marca.objects.all(),
#        error_messages={'invalid_choice': 'Opcion no valida'},
#        widget=forms.Select(attrs={'class': 'accounts-register-form-field'}))

    def clean_nombre(self):
        data = self.cleaned_data['nombre']
        if data == 'Nombre':
            raise forms.ValidationError("Es necesario un Nombre")
        return data

    def clean_descripcion(self):
        data = self.cleaned_data['descripcion']
        if data == 'Descripcion':
            raise forms.ValidationError("Es necesario una descripción")
        return data
