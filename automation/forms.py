
from django import forms
from django.forms import ModelForm
from masterdata.models import MasterData
from .models import BackupConfig


class PushConfig(ModelForm):
    class Meta:
        model = MasterData
        fields = [
            'device_type',
        ]

class PushForm(forms.Form):
    ip_address = forms.CharField()

class UploadBacukp(ModelForm):
    class Meta:
        model = BackupConfig
        fields = [
            'target',
            'b_file',
            'status',
            'time',
            'messages',
        ]