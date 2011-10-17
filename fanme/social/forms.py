# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from fanme.social.models import Evento


class MessageForm(forms.Form):
#    user_to_id = forms.CharField(
#        label='Para',
#        required=True,
#        error_messages={'required': 'Es necesario un Usuario'},
#        widget=forms.TextInput(attrs={'class': 'message-content-mati-to'}))
    user_to_id = forms.ModelChoiceField(queryset=None)
    mensaje = forms.CharField(
        label='Mensaje',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'style': 'resize: none;',
            'cols': 80, 'rows': 4}))


class MessageResponseForm(forms.Form):
    mensaje = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'style': 'resize: none;',
            'cols': 78, 'rows': 2}))


class EventoForm(forms.ModelForm):

    class Meta():
        model = Evento
        fields = (
            'fecha_inicio',
            'fecha_fin',
            'localizacion',
            'descripcion',
            'invitados'
            )
