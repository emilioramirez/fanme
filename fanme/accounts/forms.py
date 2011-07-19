#~ Definition of the accounts forms
from django import forms
#~ from django.contrib.auth.models import User

class UserRegisterForm(forms.Form):
    username = forms.CharField(label='', initial='Nombre de usuario', required=True)
    birthDate = forms.DateField(label='', initial='Fecha de Nacimiento')
    TYPES_OF_SEX = ( ('M','Masculino'), ('F','Femenino') )
    sex = forms.ChoiceField(choices=TYPES_OF_SEX)
    email = forms.EmailField(label='', initial='Email')
    password = forms.CharField(label='', initial='Password', widget=forms.PasswordInput)

