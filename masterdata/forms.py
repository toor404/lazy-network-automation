from cProfile import label
from tkinter import Widget
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms

from .models import MasterData, LOVType, LOV

class AddData(ModelForm):
    class Meta:
        model = MasterData
        fields = [
            'ip_address',
            'name',
            'device_type',
            'device_vendor',
            'ssh_port',
            'ssh_user',
            'ssh_pwd',
            'snmp_port',
            'snmp_ver',
            'snmp_community',
            'snmp_pwd',
        ]
        
        labels = {
            'ip_address':'IP Address',
        }
        widgets = {
            'ip_address': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'127.0.0.1',
                }
            ),
            
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Router Core',
                }
            ),
            
            'device_type': forms.Select(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'device_vendor': forms.Select(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'ssh_port': forms.TextInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'ssh_user': forms.TextInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'ssh_pwd': forms.TextInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'snmp_port': forms.TextInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'snmp_ver': forms.Select(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'snmp_community': forms.TextInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            
            'snmp_pwd': forms.TextInput(
                attrs = {
                    'class':'form-control',
                }
            ),
            
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter LOV sesuai tipe
        self.fields['device_type'].queryset = LOV.objects.filter(type=LOVType.DEVICE_TYPE)
        self.fields['device_vendor'].queryset = LOV.objects.filter(type=LOVType.DEVICE_VENDOR)
        self.fields['snmp_ver'].queryset = LOV.objects.filter(type=LOVType.SNMP_VERSION)

        # Tambahkan placeholder default
        self.fields['device_type'].empty_label = "Select Device Type"
        self.fields['device_vendor'].empty_label = "Select Device Vendor"
        self.fields['snmp_ver'].empty_label = "Select SNMP Version"

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

class LOVForm(forms.ModelForm):
    type = forms.ChoiceField(choices=LOVType.choices, label="LOV Type")
    value = forms.CharField(max_length=50, label="Value")

    class Meta:
        model = LOV
        fields = ["type", "value"]

    def clean(self):
        cleaned_data = super().clean()
        lov_type = cleaned_data.get("type")
        value = cleaned_data.get("value")

        if LOV.objects.filter(type=lov_type, value=value).exists():
            raise forms.ValidationError("A LOV with this type and value already exists.")

        return cleaned_data


def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter LOV sesuai tipe
        self.fields['device_type'].queryset = LOV.objects.filter(type=LOVType.DEVICE_TYPE)
        self.fields['device_vendor'].queryset = LOV.objects.filter(type=LOVType.DEVICE_VENDOR)
        self.fields['snmp_ver'].queryset = LOV.objects.filter(type=LOVType.SNMP_VERSION)

        # Tambahkan placeholder default
        self.fields['device_type'].empty_label = "Select Device Type"
        self.fields['device_vendor'].empty_label = "Select Device Vendor"
        self.fields['snmp_ver'].empty_label = "Select SNMP Version"