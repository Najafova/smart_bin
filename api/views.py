from django.shortcuts import render
from parkplace.models import * 
from django.http import JsonResponse, HttpResponse


def bins(request):
    setting_instance = DeviceSettings.objects.all()
    bin_instance = DeviceData.objects.all()
    data = []
    device_list = []

    for device in bin_instance:
        device_list.append(device.deviceName)

    print(device_list)
    
    for setting in setting_instance:
        for bin in bin_instance:
            if setting.deviceName in device_list:
                if setting.deviceName == bin.deviceName:
                    data.append({
                        'id': setting.id,
                        'deviceName': setting.deviceName,
                        'latitude': setting.latitude,
                        'longitude': setting.longitude,
                        'battery': bin.battery,
                        'bin_state': bin.bin_state,
                        'fire': bin.fire,
                    })
            elif setting.deviceName not in device_list:
                data.append({
                        'id': setting.id,
                        'deviceName':setting.deviceName,
                        'latitude': setting.latitude,
                        'longitude': setting.longitude,
                        'battery': 0,
                        'bin_state': 0,
                        'fire': 0,
                    })
    return JsonResponse(data, safe=False)


def start_point(request):
    setting_coordinates = StartPoint.objects.all()
    data = []

    for coordinate in setting_coordinates:
        data.append({
            'latitude': coordinate.latitude,
            'longitude': coordinate.longitude,
        })
    return JsonResponse(data, safe=False)