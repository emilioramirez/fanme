# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

TYPES_OF_SEX = (('', 'Sexo'), ('M', 'Masculino'), ('F', 'Femenino'))


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


class UserUpdateForm(forms.Form):
    first_name = forms.CharField(
        label='Nombre',
        required=True,
        error_messages={'required': 'Es necesario un Nombre'},
        widget=forms.TextInput(attrs={'class': 'edit-account-form-field'}))
    last_name = forms.CharField(
        label='Apellido',
        required=True,
        error_messages={'required': 'Es necesario un Apellido'},
        widget=forms.TextInput(attrs={'class': 'edit-account-form-field'}))
    sex = forms.ChoiceField(
        label='Sexo',
        choices=TYPES_OF_SEX,
        error_messages={'required': 'Es necesario su Sexo',
            'invalid_choice': 'Opcion no valida, seleccioe M o F'},
        widget=forms.Select(attrs={'class': 'edit-account-combo-field'}))
    email = forms.EmailField(
        label='Email',
        error_messages={'required': 'Es necesario su Email',
            'invalid': 'Correo electronico no valido'},
        widget=forms.TextInput(attrs={'class': 'edit-account-email-field'}))
    birth_date = forms.DateField(
        label='Fecha de Nacimiento',
        initial='',
        input_formats=['%d/%m/%Y'],
        error_messages={'required': 'Fecha invalida, ingrese de la forma Día/Mes/Año',
            'invalid': 'Fecha invalida, ingrese de la forma Día/Mes/Año'},
        widget=forms.DateInput(attrs={'class': 'edit-account-date-field'}))

    def clean_username(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            raise forms.ValidationError("Este usuario ya existe")
        except User.DoesNotExist:
            pass
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if data == 'Nombre':
            raise forms.ValidationError("Es necesario un Nombre")
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if data == 'Apellido':
            raise forms.ValidationError("Es necesario un Apellido")
        return data


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
