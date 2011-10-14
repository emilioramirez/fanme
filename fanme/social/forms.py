# -*- coding: utf-8 *-*
from django.forms import ModelForm
from fanme.social.models import Evento


class EventoForm(ModelForm):
    class Meta():
        model = Evento
