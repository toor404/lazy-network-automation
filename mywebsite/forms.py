from cProfile import label
from tkinter import Widget
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'class':'form-control form-control-lg bg-white bg-opacity-5',
                    'placeholder':'user1'
                }
            ),
            'email': forms.EmailInput(
                attrs = {
                    'class':'form-control form-control-lg bg-white bg-opacity-5',
                    'placeholder':'user1@netter.co.id'
                }
            ),
            'password1': forms.PasswordInput(
                attrs = {
                    'class':'form-control form-control-lg bg-white bg-opacity-5'
                }
            ),
            'password2': forms.PasswordInput(
                attrs = {
                    'class':'form-control form-control-lg bg-white bg-opacity-5'
                }
            )
        }