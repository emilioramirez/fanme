# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User

TYPES_OF_SEX = (('', 'Sexo'), ('M', 'Masculino'), ('F', 'Femenino'))


class SearchBox(forms.Form):
    string = forms.CharField(label='',
        required=False,
        widget=forms.TextInput(attrs={'class': 'header-seach-form-field', 'placeholder': "Buscar"}))

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
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        label='Apellido',
        required=True,
        error_messages={'required': 'Es necesario un Apellido'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(
        label='Sexo',
        choices=TYPES_OF_SEX,
        error_messages={'required': 'Es necesario su Sexo',
            'invalid_choice': 'Opcion no valida, seleccioe M o F'},
        widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(
        label='Email',
        error_messages={'required': 'Es necesario su Email',
            'invalid': 'Correo electronico no valido'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}))
    birth_date = forms.DateField(
        label='Fecha de Nacimiento',
        initial='',
        input_formats=['%d/%m/%Y'],
        error_messages={'required': 'Fecha invalida: Día/Mes/Año',
            'invalid': 'Fecha invalida: Día/Mes/Año'},
        widget=forms.DateInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(
        required=False,
        label='Imagen de Perfil',
        )

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

    def __init__(self, user, data=None):
        self.user = user
        super(PassUpdateForm, self).__init__(data=data)

    def clean_new_pass(self):
        data = self.cleaned_data['new_pass']
        try:
            User.objects.get(password=data)
            raise forms.ValidationError("Este usuario ya existe")
        except User.DoesNotExist:
            pass
        return data

    def clean_actual_pass(self):
        data = self.cleaned_data['actual_pass']
        if not self.user.check_password(data):
            raise forms.ValidationError("La contraseña actual ingresada no coincide.")
            print 'hola'
        return data
