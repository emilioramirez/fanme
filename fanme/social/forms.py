# -*- coding: utf-8 *-*
from django import forms
from fanme.social.models import Evento


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
