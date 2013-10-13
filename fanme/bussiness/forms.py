# -*- coding: utf-8 -*-
from django import forms


class NotificacionForm(forms.Form):
#    user_to_id = forms.CharField(
#        label='Para',
#        required=True,
#        error_messages={'required': 'Es necesario un Usuario'},
#        widget=forms.TextInput(attrs={'class': 'message-content-mati-to'}))
    user_to_id = forms.MultipleChoiceField(
        label='Mensaje',
        required=True)
    descripcion = forms.CharField(
        label='Descripcion',
        initial='',
        required=True,
        error_messages={'required': 'Es necesario una Descripcion'},
        widget=forms.Textarea
            (attrs={'style': 'resize: none;', 'cols': 80, 'rows': 4}))
#    url = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoNotificacion)
    leido = models.BooleanField()
    resumen = models.CharField(max_length=50)
