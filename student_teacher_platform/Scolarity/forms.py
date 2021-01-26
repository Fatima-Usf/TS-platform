# -*- coding: utf-8 -*-
from Scolarity.choices import SEXE
from django import forms

from .models import Etudiant
from django.contrib.auth.models import User

"""
class InscriptionEtudiant(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ["nom", "prenom", "dateNaissance", "sexe", "adrs", "nationality", "tel", "mail", "user"]
        widgets = {
            'nom': forms.TextInput(
                attrs={'class': 'form-control',
                       'type': 'text',
                       'required': 'required'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control',
                                       'type': 'text',
                                       'required': 'required'}),
            'dateNaissance': forms.TextInput(attrs={'class': 'form-control',
                                              'type': 'date',
                                              'required': 'required'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control',
                                            'type': 'text',
                                            'required': 'required'}),
            'sexe': forms.Select(attrs={'class': 'custom-select d-block w-100',
                                  'required': 'required'}),
            'mail': forms.EmailInput(attrs={'class': 'form-control',
                                      'type': 'email',
                                      'required': 'required'}),
            'tel': forms.TextInput(attrs={'class': 'form-control',
                                    'type': 'tel',
                                    'required': 'required'}),
            'adrs': forms.TextInput(attrs={'class': 'form-control',
                                     'type': 'text',
                                     'required': 'required'}),
        }

class AddUser(ModelForm):
    class Meta:
        model: User
        fields = ['username', 'password']
        widgets = {'username': TextInput(attrs={'class': 'form-control',
                                                'type': 'text',
                                                'required': 'required'}),
                    'password': PasswordInput(attrs={'class': 'form-control',
                                                    'type': 'password',
                                                    'required': 'required'}),
        }
"""

class InscriptionEtudiant(forms.Form):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'required': 'required'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'required': 'required'}))
    sexe = forms.ChoiceField(choices=SEXE, widget=forms.Select(attrs={'class': 'custom-select d-block w-100', 'required': 'required'}))
    dateNaissance = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'date', 'required': 'required'}))
    nationality = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'required': 'required'}))
    mail = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'required': 'required'}))
    tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'tel', 'required': 'required'}))
    adrs = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'required': 'required'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'required': 'required'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'required'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'required'}))
