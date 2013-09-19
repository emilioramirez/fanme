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
    user_to_id = forms.ModelChoiceField(queryset=None)
    mensaje = forms.CharField(
        label='Mensaje',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea(attrs={
                'class': 'item-registration-description-field'}))


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
        widget=forms.Select(attrs={'class': 'combo-item'}))
    consulta = forms.CharField(
        label='Consulta',
        required=True,
        error_messages={'required': 'Es necesario ingresar un mensaje'},
        widget=forms.Textarea(attrs={'class': 'new-message-field'}))


class EventoForm(forms.ModelForm):

    class Meta():
        model = Evento
        fields = (
            'nombre',
            'tipo',
            'fecha_inicio',
            'fecha_fin',
            'localizacion',
            'descripcion',
            'invitados',
            'imagen',
            )
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'evento-date-form-field field-evento-new'}),
            'fecha_fin': forms.DateInput(attrs={
                'class': 'evento-date-form-field field-evento-new'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'evento-date-form-field field-evento-new'}),
        }


class NotificationForm(forms.ModelForm):

    class Meta():
        model = Notificacion
        fields = (
            'nombre',
            'fecha_desde',
            'fecha_expiracion',
            'descripcion',
            'usuarios_to',
            'imagen',
            )
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'notification-name-field'}),
            'fecha_desde': forms.DateTimeInput(attrs={
                'class': 'notification-name-field'}),
            'fecha_expiracion': forms.DateTimeInput(attrs={
                'class': 'notification-name-field'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'new-notification-textarea'}),
        }
