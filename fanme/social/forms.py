# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from fanme.social.models import Evento, Notificacion
import datetime


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
            'cols': 60, 'rows': 4}))


class MessageResponseForm(forms.Form):
    mensaje = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'style': 'resize: none;',
            'widht': 80, 'rows': 2}))


class MessageQueryForm(forms.Form):
    mensaje = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'style': 'resize: none;  margin: -16px 67px;',
            'cols': 78, 'rows': 5}))


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
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'evento-date-form-field field-evento-new'}),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'evento-date-form-field field-evento-new'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'evento-date-form-field field-evento-new'}),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        fecha_inicio = cleaned_data['fecha_inicio']
        fecha_fin = cleaned_data['fecha_fin']
        if fecha_inicio < datetime.date.today():
            raise forms.ValidationError(
                'La fecha de inicio es menor que la fecha actual')
        if fecha_fin < fecha_inicio:
            raise forms.ValidationError(
                'La fecha de fin no puede ser menor que la fecha inicio')
        return cleaned_data


class NotificationForm(forms.ModelForm):

    class Meta():
        model = Notificacion
        fields = (
            'nombre',
            'fecha_expiracion',
            'descripcion',
            'usuarios_to',
            )
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'notification-name-field'}),
            'fecha_expiracion': forms.DateInput(attrs={
                'class': 'notification-name-field'}),
            'descripcion': forms.Textarea(attrs={
                'style': 'resize: none;',
                'cols': 50, 'rows': 4}),
        }
