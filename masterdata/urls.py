from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('lov/', views.lov, name='lov'),
    path('', views.index, name='home'),
]
