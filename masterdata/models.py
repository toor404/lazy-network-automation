from email.policy import default
from django.db import models


# Create your models here.


class LOVType(models.TextChoices):
    DEVICE_TYPE = "device_type", "Device Type"
    DEVICE_VENDOR = "device_vendor", "Device Vendor"
    SNMP_VERSION = "snmp_version", "SNMP Version"

class LOV(models.Model):
    type = models.CharField(max_length=20, choices=LOVType.choices)
    value = models.CharField(max_length=50)
    
    def __str__(self):
        return self.value

class MasterData(models.Model):
    ip_address = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    device_type = models.ForeignKey(LOV, on_delete=models.CASCADE, related_name='device_types')
    device_vendor = models.ForeignKey(LOV, on_delete=models.CASCADE, related_name='device_vendors')
    snmp_ver = models.ForeignKey(LOV, on_delete=models.CASCADE, related_name='snmp_versions')
    created = models.DateTimeField(auto_now_add=True)
    ssh_user = models.CharField(max_length=256)
    ssh_pwd = models.CharField(max_length=256)
    ssh_port = models.IntegerField(default=22)
    enab_pwd = models.CharField(max_length=256, blank=True)
    snmp_port = models.IntegerField(default=161, blank=True)
    snmp_community = models.CharField(max_length=256, blank=True)
    snmp_pwd = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return f"{self.ip_address} | {self.name} | {self.device_type} | {self.device_vendor}"


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