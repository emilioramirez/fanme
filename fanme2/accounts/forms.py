# -*- coding: utf-8 *-*
from django import forms
from accounts.models import ProfileUser


class ProfileUserForm(forms.ModelForm):
    class Meta:
        model = ProfileUser
        exclude = ('user', 'first_login')
