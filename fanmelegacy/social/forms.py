# -*- coding: utf-8 -*-
from django import forms
from social.models import Evento, Notificacion
from items.models import Item


class MessageForm(forms.Form):
#    user_to_id = forms.CharField(
#        label='Para',
#        required=True,
#        error_messages={'required': 'Es necesario un Usuario'},
#        widget=forms.TextInput(attrs={'class': 'message-content-mati-to'}))
    user_to_id = forms.ModelChoiceField(queryset=None,
        widget=forms.Select(attrs={
                'class': 'form-control'}))
    mensaje = forms.CharField(
        label='Mensaje',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea(attrs={
                'class': 'form-control'}))


class MessageResponseForm(forms.Form):
    mensaje = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'class': 'response-message-field'}))


class MessageQueryForm(forms.Form):
    item = forms.ModelChoiceField(
        label='',
        empty_label="---",
        queryset=Item.objects.all(),
        error_messages={'required': 'Es necesario un Item',
            'invalid_choice': 'Opcion no valida'},
        widget=forms.Select(attrs={'class': 'form-control'}))
    consulta = forms.CharField(
        label='Consulta',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea(attrs={'class': 'form-control'}))


class EventoForm(forms.ModelForm):

    class Meta():
        model = Evento
        fields = (
            'nombre',
            'tipo',
            'fecha_inicio',
            'fecha_fin',
            'descripcion',
            'invitados',
            'imagen',
            'direccion',
            )
        widgets = {
           'nombre': forms.TextInput(attrs={
                'class': 'form-control'}),
            'tipo': forms.Select(attrs={
                'class': 'form-control'}),
             'fecha_inicio': forms.DateTimeInput(attrs={
                'class': 'form-control'}),
             'fecha_fin': forms.DateTimeInput(attrs={
                'class': 'form-control'}),
             'descripcion': forms.Textarea(attrs={
                'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control'}),
        }


class NotificationForm(forms.ModelForm):

    class Meta():
        model = Notificacion
        fields = (
            'nombre',
            'fecha_desde',
            'fecha_expiracion',
            'descripcion',
            'imagen',
            )
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control'}),
            'fecha_desde': forms.DateTimeInput(attrs={
                'class': 'form-control'}),
            'fecha_expiracion': forms.DateTimeInput(attrs={
                'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control'})
        }


class ConsultaResponseForm(forms.Form):
    respuesta = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea
            (attrs={'class': 'response-message-field'}))
