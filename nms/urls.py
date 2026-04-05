from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('devices/', views.device_API, name='home'),
    #path('admin/', admin.site.urls),
]
