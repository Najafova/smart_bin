from django.contrib import admin
from .models import *

# admin.site.register(Place)
# admin.site.register(Reserves)
# Register your models here.


@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ['deviceName', 'battery', 'bin_state', 'fire']
    search_fields = ['deviceName']
    list_filter = ['deviceName']

@admin.register(DeviceSettings)
class DeviceSettingsAdmin(admin.ModelAdmin):
    list_display = ['deviceName', 'latitude', 'longitude']
    search_fields = ['deviceName', 'latitude', 'longitude']
    list_filter = ['deviceName']

@admin.register(LogData)
class LogDataAdmin(admin.ModelAdmin):
    list_display = ['deviceName', 'battery', 'bin_state', 'fire', 'request_time']
    search_fields = ['deviceName']
    list_filter = ['deviceName']


@admin.register(StartPoint)
class StartPointAdmin(admin.ModelAdmin):
    list_display = ['latitude', 'longitude']