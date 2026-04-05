from django import forms
from dataclasses import field
import django_filters
from .models import Log

from masterdata.models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = MasterData
        fields = [
            'device_type',
            'device_vendor',
            
        ] 
        
class LogFilter(django_filters.FilterSet):
    class Meta:
        model = Log
        fields = [
            'target',
            'action',
            'status',
            
            
        ] 
        
