# -*- coding: utf-8 *-*
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from support.models import Rubro

TYPES_OF_SEX = (('', 'Sexo'), ('M', 'Masculino'), ('F', 'Femenino'))


class UserLogin(forms.Form):
    login_username = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario su Email'},
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    login_password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}),
            error_messages={'required': 'Es necesario una Password'})

    def clean(self):
        login_username = self.cleaned_data.get('login_username')
        login_password = self.cleaned_data.get('login_password')
        if login_username and login_password:
            user = authenticate(username=login_username,
                password=login_password)
            if user is None:
                raise forms.ValidationError("Usuario o Password no valido")
        return self.cleaned_data


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario un Nombre'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field',
            'placeholder': 'Nombre'})
        )
    last_name = forms.CharField(
        label='',
        required=True,
        error_messages={'required': 'Es necesario un Apellido'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field',
            'placeholder': 'Apellido'})
        )
    birth_date = forms.DateField(
        label='',
        input_formats=['%d/%m/%Y'],
        error_messages={'required': 'Es necesaria su Fecha de Nacimiento',
            'invalid': u'Fecha invalida, ingrese de la forma Día/Mes/Año'},
        widget=forms.DateInput(attrs={'class': 'accounts-register-form-field',
            'placeholder': 'Fecha de Nacimiento'})
        )
    sex = forms.ChoiceField(
        label='',
        choices=TYPES_OF_SEX,
        error_messages={'required': 'Es necesario su Sexo',
            'invalid_choice': 'Opcion no valida, seleccioe M o F'},
        widget=forms.Select(attrs={'class': 'accounts-register-form-field',
            'placeholder': 'Sexo'})
        )
    email = forms.EmailField(
        label='',
        error_messages={'required': 'Es necesario su Email',
            'invalid': 'Correo electronico no valido'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field',
            'placeholder': 'Email'})
        )
    password = forms.CharField(
        label='',
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'accounts-register-form-field',
            'placeholder': 'Password'}),
        error_messages={'required': 'Es necesario una Password',
            'min_length': 'Debe ingresar minimo 6 caracteres'})

    def clean_email(self):
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


class CompanyRegisterForm(forms.Form):
    razon_social = forms.CharField(
        label='',
        initial='Razon Social',
        required=True,
        error_messages={'required': 'Es necesario una Razón Social'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    direccion = forms.CharField(
        label='',
        initial='Direccion',
        required=True,
        error_messages={'required': 'Es necesario una Dirección'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    rubro = forms.ModelChoiceField(
        label='',
        empty_label="Rubro",
        queryset=Rubro.objects.all(),
        error_messages={'required': 'Es necesario un Rubro',
            'invalid_choice': 'Opcion no valida'},
        widget=forms.Select(attrs={'class': 'accounts-register-form-field'}))
    url = forms.URLField(
        label='',
        initial='Página Web',
        error_messages={'required': 'Es necesario su Página web',
        'invalid': 'Página web no válida'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    email = forms.EmailField(
        label='',
        initial='Email',
        error_messages={'required': 'Es necesario su Email',
            'invalid': 'Correo electronico no valido'},
        widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    password = forms.CharField(
        label='',
        initial='Password',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'accounts-register-form-field'}),
            error_messages={'required': 'Es necesario una Password'})

    def clean_username(self):
        data = self.cleaned_data['email']
        try:
            User.objects.get(email=data)
            raise forms.ValidationError("Este usuario ya existe")
        except User.DoesNotExist:
            pass
        return data

    def clean_razon_social(self):
        data = self.cleaned_data['razon_social']
        if data == 'Razon Social':
            raise forms.ValidationError("Es necesario una Razón Social")
        return data

    def clean_direccion(self):
        data = self.cleaned_data['direccion']
        if data == 'Direccion':
            raise forms.ValidationError("Es necesario una Dirección")
        return data
