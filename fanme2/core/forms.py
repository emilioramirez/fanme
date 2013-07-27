# -*- coding: utf-8 *-*
from django import forms
from core.models import Item, Topico, Evento, Notificacion
from django.contrib.auth.models import User


#Inicio Sección: Forms que migran desde fanme.dash
class SearchBox(forms.Form):
    string = forms.CharField(label='',
        initial='Buscar',
        required=False,
        widget=forms.TextInput(attrs={'class': 'header-seach-form-field'}))

    def clean_string(self):
        string = self.cleaned_data['string']
        if string == "":
            raise forms.ValidationError("Debe ingresar una palabra")
        return string


class PassUpdateForm(forms.Form):
    actual_pass = forms.CharField(
        label='Contraseña Actual',
        initial='',
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'edit-account-form-field'}),
        error_messages={'required': 'Es necesario una Password',
            'min_length': 'Debe ingresar minimo 6 caracteres'})
    new_pass = forms.CharField(
        label='Contraseña Nueva',
        initial='',
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'edit-account-form-field'}),
        error_messages={'class': 'errorlist-pass',
            'required': 'Es necesario una Password',
            'min_length': 'Debe ingresar minimo 6 caracteres'})

    def clean_new_pass(self):
        data = self.cleaned_data['new_pass']
        try:
            User.objects.get(password=data)
            raise forms.ValidationError("Este usuario ya existe")
        except User.DoesNotExist:
            pass
        return data

#Fin Sección.


#Inicio Sección: Forms que migran desde fanme.items
class ItemRegisterForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre',
        initial='',
        required=True,
        error_messages={'required': 'Es necesario un Nombre'},
        widget=forms.TextInput(attrs={'class': 'item-registration-name-field'}))
    descripcion = forms.CharField(
        label='Descripción (máx. 300 caracteres)',
        initial='',
        required=True,
        error_messages={'required': 'Es necesario una descripción'},
        widget=forms.Textarea
            (attrs={'class': 'item-registration-description-field'}))
    topico = forms.ModelChoiceField(
        label='Tópico',
        empty_label="Tópico",
        queryset=Topico.objects.all(),
        error_messages={'required': 'Es necesario un Tópico',
            'invalid_choice': 'Opcion no valida'},
        widget=forms.Select(attrs={'class': 'item-registration-combo-field'}))
#TODO: ver si realmente vamos a estar relacionandolo con una marca o no.
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
#Fin Sección.


#Inicio Sección: Forms que migran desde fanme.social
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
            )
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'notification-name-field'}),
            'fecha_desde': forms.DateInput(attrs={
                'class': 'notification-name-field'}),
            'fecha_expiracion': forms.DateInput(attrs={
                'class': 'notification-name-field'}),
            'descripcion': forms.Textarea(attrs={
                'class': 'new-notification-textarea'}),
        }
#Fin Sección.
