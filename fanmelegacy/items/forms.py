# -*- coding: utf-8 -*-
from django import forms
#from django.contrib.auth import authenticate
from items.models import Marca, Item
from segmentation.models import Topico


class ItemRegisterForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        initial='',
        required=True,
        error_messages={'required': 'Es necesario un Nombre'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    descripcion = forms.CharField(
        label='Descripción (máx. 300 caracteres)',
        initial='',
        required=True,
        error_messages={'required': 'Es necesario una descripción'},
        widget=forms.Textarea
            (attrs={'class': 'form-control'}))
    topico = forms.ModelChoiceField(
        label='Tópico',
        empty_label="Tópico",
        queryset=Topico.objects.all(),
        error_messages={'required': 'Es necesario un Tópico',
            'invalid_choice': 'Opcion no valida'},
        widget=forms.Select(attrs={'class': 'form-control'}))
#    marca = forms.ModelChoiceField(
#        label='Marca',
#        empty_label="Marca",
#        queryset=Marca.objects.all(),
#        required=False,
#        error_messages={'invalid_choice': 'Opcion no valida'},
#        widget=forms.Select(attrs={'class': 'item-registration-combo-field'}))
    imagen = forms.ImageField(
        required=True,
        label='Imagen del Item',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
        )

    def clean_nombre(self):
        data = self.cleaned_data['nombre']
        try:
            Item.objects.get(nombre=data)
            raise forms.ValidationError("Este item ya existe")
        except Item.DoesNotExist:
            pass
        return data

    def clean_descripcion(self):
        data = self.cleaned_data['descripcion']
        if data == 'Descripcion':
            raise forms.ValidationError("Es necesario una descripción")
        return data


class CommentForm(forms.Form):
    texto = forms.CharField(
        label='',
        initial='Ingrese su comentario aquí',
        required=True,
        error_messages={'required': 'Es necesario un comentario'},
        widget=forms.Textarea(attrs={'class': 'comment-text-add'}))

    def clean_texto(self):
        data = self.cleaned_data['texto']
        if data == u'Ingrese su comentario aquí':
            raise forms.ValidationError("Es necesario un comentario")
        return data
