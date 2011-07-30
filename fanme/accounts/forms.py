# -*- coding: utf-8 -*-
#~ Definition of the accounts forms
from django import forms
from django.contrib.auth.models import User
from fanme.support.models import Rubro

TYPES_OF_SEX = (('','Sexo'),('M', 'Masculino'), ('F', 'Femenino'))

class UserLogin(forms.Form):
    login_username = forms.CharField(label='',
                               initial='Email',
                               required=False)
    login_password = forms.CharField(label='',
                               initial='Password',
                               required=False,
                               widget=forms.PasswordInput())

    #~ def clean_login_username(self):
        #~ data = self.cleaned_data['login_username']
        #~ try:
            #~ user = User.objects.get(login_username=data)
            #~ pass
        #~ except User.DoesNotExist:
            #~ raise forms.ValidationError("Este usuario no existe")
        #~ return data


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(label='',
                               initial='Nombre',
                               required=True,
                               error_messages={'required': 'Es necesario un Nombre'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    last_name = forms.CharField(label='',
                               initial='Apellido',
                               required=True,
                               error_messages={'required': 'Es necesario un Apellido'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    birth_date = forms.DateField(label='',
                                 initial='Fecha de Nacimiento',
                                 input_formats=['%d/%m/%Y'],
                                 error_messages={'required': 'Es necesaria su Fecha de Nacimiento',
                                 'invalid': 'Fecha invalida, ingrese de la forma Día/Mes/Año'},
                                 widget=forms.DateInput(attrs={'class': 'accounts-register-form-field'}))
    sex = forms.ChoiceField(label='',
                            choices=TYPES_OF_SEX,
                            error_messages={'required': 'Es necesario su Sexo',
                                 'invalid_choice': 'Opcion no valida, seleccioe M o F'},
                            widget=forms.Select(attrs={'class': 'accounts-register-form-field'}))
    email = forms.EmailField(label='',
                             initial='Email',
                             error_messages={'required': 'Es necesario su Email',
                                 'invalid': 'Correo electronico no valido'},
                             widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    password = forms.CharField(label='',
                               initial='Password',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'accounts-register-form-field'}),
                               error_messages={'required': 'Es necesario una Password',
                               'min_length': 'Debe ingresar minimo 6 caracteres'})

    def clean_username(self):
        data = self.cleaned_data['email']
        try:
            user = User.objects.get(email=data)
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
    #~ username = forms.CharField(label='',
                               #~ initial='Nombre de usuario',
                               #~ required=True,
                               #~ error_messages={'required': 'Es necesario un nombre de Usuario'},
                               #~ widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    razon_social = forms.CharField(label='',
                               initial='Razon Social',
                               required=True,
                               error_messages={'required': 'Es necesario una Razón Social'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    direccion = forms.CharField(label='',
                               initial='Direccion',
                               required=True,
                               error_messages={'required': 'Es necesario una Dirección'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    rubro = forms.ModelChoiceField(label='',
                                   empty_label="Rubro",
                                   queryset=Rubro.objects.all(),
                                   error_messages={'required': 'Es necesario un Rubro',
                                   'invalid_choice': 'Opcion no valida'},
                                   widget=forms.Select(attrs={'class': 'accounts-register-form-field'}))
    url = forms.URLField(label='',
                             initial='Página Web',
                             verify_exists=False,
                             error_messages={'required': 'Es necesario su Página web',
                                 'invalid': 'Página web no válida'},
                             widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    email = forms.EmailField(label='',
                             initial='Email',
                             error_messages={'required': 'Es necesario su Email',
                                 'invalid': 'Correo electronico no valido'},
                             widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    password = forms.CharField(label='',
                               initial='Password',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class': 'accounts-register-form-field'}),
                               error_messages={'required': 'Es necesario una Password'})

    def clean_username(self):
        data = self.cleaned_data['email']
        try:
            user = User.objects.get(email=data)
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
