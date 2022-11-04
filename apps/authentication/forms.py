from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.home.models import *





class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ingrese nombre de usuario",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Ingrese contraseña",
                "class": "form-control"
            }
        ))



class CustomerUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2", "is_staff"] 
        labels = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            'first_name': forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'type':'text'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'type':'email'}),
            'password1': forms.TextInput(attrs={'class':'form-control', 'type':'password'}),
            'password2': forms.TextInput(attrs={'class':'form-control', 'type':'password'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'required checkbox form-control'})
        }