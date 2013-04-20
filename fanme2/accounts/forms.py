# -*- coding: utf-8 *-*
from django import forms
from accounts.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # exclude = ('user', 'first_login')


# class ProfileUserForm(forms.ModelForm):
#     class Meta:
#         model = ProfileUser
    
