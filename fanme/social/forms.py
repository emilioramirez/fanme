# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User


class MessageForm(forms.Form):
    user_to_id = forms.CharField(
        label='Para',
        required=True,
        error_messages={'required': 'Es necesario un Usuario'},
        widget=forms.TextInput(attrs={'class': 'message-content-mati-to'}))
    mensaje = forms.CharField(
        label='Mensaje',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'class': 'message-content-mati-desciption',
            'cols': 80, 'rows': 4}))
