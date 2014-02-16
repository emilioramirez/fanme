# forms.py
from django import forms
from segmentation.models import AnalisisDenuncia


class AnalisisDenunciaForm(forms.ModelForm):
    class Meta:
        model = AnalisisDenuncia
        fields = ('estado', 'descripcion')