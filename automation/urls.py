from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('backup_list/', views.fb_list),
    path('backup_config/', views.backup_config),
    path('verify_config/', views.verify_config),
    path('history/', views.history),
    path('push_config/', views.push_config),
    path('', views.index),
    
]
