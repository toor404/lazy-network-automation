from django.contrib import admin

# Register your models here.
from .models import MasterData, LOV


admin.site.register(MasterData)
admin.site.register(LOV)