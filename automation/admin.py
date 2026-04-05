from django.contrib import admin

# Register your models here.
from .models import Log, BackupConfig

admin.site.register(Log)
admin.site.register(BackupConfig)