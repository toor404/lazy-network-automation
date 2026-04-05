from django import forms
import django_filters
from .models import Log
from masterdata.models import MasterData, LOV, LOVType


class OrderFilter(django_filters.FilterSet):
    device_type = django_filters.ModelChoiceFilter(
        queryset=LOV.objects.filter(type=LOVType.DEVICE_TYPE),
        empty_label='All Types',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )
    device_vendor = django_filters.ModelChoiceFilter(
        queryset=LOV.objects.filter(type=LOVType.DEVICE_VENDOR),
        empty_label='All Vendors',
        widget=forms.Select(attrs={'class': 'form-select form-select-sm'}),
    )

    class Meta:
        model = MasterData
        fields = ['device_type', 'device_vendor']


class LogFilter(django_filters.FilterSet):
    target = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'IP Address'}),
    )
    action = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Action'}),
    )
    status = django_filters.CharFilter(
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Status'}),
    )

    class Meta:
        model = Log
        fields = ['target', 'action', 'status']
        
