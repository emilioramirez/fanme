# -*- coding: utf-8 -*-
#~ Definition of the accounts forms
from django import forms
from django.contrib.auth.models import User
from fanme.soport.models import Rubro

TYPES_OF_SEX = (('Sexo','Sexo'),('M', 'Masculino'), ('F', 'Femenino'))

class UserLogin(forms.Form):
    login_username = forms.CharField(label='',
                               initial='Nombre de usuario',
                               required=False)
    login_password = forms.CharField(label='',
                               initial='Password',
                               required=False,
                               widget=forms.PasswordInput())

class UserRegisterForm(forms.Form):
    username = forms.CharField(label='',
                               initial='Nombre de usuario',
                               required=True,
                               error_messages={'required': 'Es necesario un nombre de Usuario'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    birth_date = forms.DateField(label='',
                                 initial='Fecha de Nacimiento',
                                 input_formats=['%d/%m/%Y'],
                                 error_messages={'required': 'Es necesaria su fecha de Nacimiento',
                                 'invalid': 'Fecha invalida, ingrese de la forma Día/Mes/Año'},
                                 widget=forms.DateInput(attrs={'class': 'accounts-register-form-field'}))
    sex = forms.ChoiceField(label='',
                            choices=TYPES_OF_SEX,
                            error_messages={'required': 'Es necesario su Sexo',
                                 'invalid_choice': 'Opcion no valida, seleccioe M o F'},
                            widget=forms.Select(attrs={'class': 'accounts-register-form-field'}))
    email = forms.EmailField(label='',
                             initial='Email',
                             error_messages={'required': 'Es necesario su correo electronico',
                                 'invalid': 'Correo electronico no valido'},
                             widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    password = forms.CharField(label='',
                               initial='Password',
                               widget=forms.PasswordInput(attrs={'class': 'accounts-register-form-field'}),
                               error_messages={'required': 'Es necesario una contraseña'})

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            user = User.objects.get(username=data)
            raise forms.ValidationError("Este usuario ya existe")
        except User.DoesNotExist:
            pass
        return data


class CompanyRegisterForm(forms.Form):
    username = forms.CharField(label='',
                               initial='Nombre de usuario',
                               required=True,
                               error_messages={'required': 'Es necesario un nombre de Usuario'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    razon_social = forms.CharField(label='',
                               initial='Razón Social',
                               required=True,
                               error_messages={'required': 'Es necesario una razón social'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    direccion = forms.CharField(label='',
                               initial='Dirección',
                               required=True,
                               error_messages={'required': 'Es necesario una dirección'},
                               widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    rubro = forms.ModelChoiceField(label='',
                                   empty_label="Rubro",
                                   queryset=Rubro.objects.all(),
                                   error_messages={'required': 'Es necesario un rubro',
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
                             error_messages={'required': 'Es necesario su correo electronico',
                                 'invalid': 'Correo electronico no valido'},
                             widget=forms.TextInput(attrs={'class': 'accounts-register-form-field'}))
    password = forms.CharField(label='',
                               initial='Password',
                               widget=forms.PasswordInput(attrs={'class': 'accounts-register-form-field'}),
                               error_messages={'required': 'Es necesario una contraseña'})

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            user = User.objects.get(username=data)
            raise forms.ValidationError("Este usuario ya existe")
        except User.DoesNotExist:
            pass
        return data
