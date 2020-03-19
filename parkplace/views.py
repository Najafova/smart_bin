import datetime
import pytz
import json
import base64

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
# from .serializers import placeSerializer

utc=pytz.UTC

def index(request):
    context = {}
    context["marker"] = DeviceData.objects.all()
    data = DeviceSettings.objects.all()
    # print(data)
    # d_data = DeviceSettings.objects.all()
    result = []
    test = []
    order = 0

    device_settings_data = DeviceSettings.objects.all()
    for item in device_settings_data:
        d_data = DeviceSettings.objects.get(deviceName=item.deviceName).bin_height
        print(d_data)

    for item in data:
        order = order + 1
        try:
            d_data = DeviceData.objects.get(deviceName=item.deviceName)
            # print(d_data.bin_state)

            if d_data.bin_state<25:
                color = "bg-success"
            elif d_data.bin_state<51:
                color = "yellow"
            elif d_data.bin_state<75:
                color = "orange"
            else:
                color = "bg-danger"
        
            result.append({
                "coords": {"lat": item.latitude, "lng": item.longitude},
                "text": "{} {} {} {} {}".format(order, item.deviceName or int(0), d_data.battery or int(0), d_data.bin_state or int(0), d_data.fire or int(0)).split(),
                # "battery": "bg-danger" if (int(d_data.bin_state) or 0) >= 75  else "bg-success",
                "battery": color,
                "device_icon": d_data.device_icon()
            })
        except DeviceData.DoesNotExist:
            result.append({
            "coords": {"lat": item.latitude, "lng":item.longitude},
            "text": "{} {} {} {} {}".format(order, item.deviceName, int(0), int(0), int(0)).split(),
            "battery": "bg-danger",
            "device_icon": "/static/wasco/images/green.png",
            })

    context["object_list"] = result
    return render(request, "index.html", context)



class Get_place_List(APIView):
    def get(self, request):
        place = Place.objects.all()
        serialized = placeSerializer(place, many=True)
        return Response(serialized.data)
@csrf_exempt
def getdata(request):
    if request.method =="POST":
        now = datetime.datetime.utcnow()+datetime.timedelta(hours=4)
        now=utc.localize(now)
        a = request.body.decode()
        data = json.loads(a)
        status = data['data']
        print('')

        my_data = base64.b64decode(data["data"]).decode('utf-8')
        coded_data = list()
        coded_data = my_data.split(",")
        if int(coded_data[0]) < 900:
            coded_data[0] = 0
        else:
            coded_data[0] = round((int(coded_data[0])-900)*100/123,1)
        
        coded_data[1] = int(coded_data[1])
        print(type(coded_data[1]))

        device_settings_data = DeviceSettings.objects.all()
        for item in device_settings_data:
            # d_data = (DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-coded_data[1]*100)/DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-coded_data[1]*100
            d_data = ((DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-coded_data[1])*100)/DeviceSettings.objects.get(deviceName=item.deviceName).bin_height
            print(d_data)


        if DeviceSettings.objects.filter(deviceName=data["deviceName"]) and DeviceData.objects.filter(deviceName=data["deviceName"]):
            if DeviceSettings.objects.get(deviceName=item.deviceName).bin_height < coded_data[1]:
                DeviceData.objects.filter(deviceName=data["deviceName"]).update(battery=coded_data[0], bin_state="-", fire=coded_data[2])
            else:
                DeviceData.objects.filter(deviceName=data["deviceName"]).update(battery=coded_data[0], bin_state=((DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-coded_data[1])*100)/DeviceSettings.objects.get(deviceName=item.deviceName).bin_height, fire=coded_data[2])
            print("Updated!")

        elif DeviceSettings.objects.filter(deviceName=data["deviceName"]) and not DeviceData.objects.filter(deviceName=data["deviceName"]):
            DeviceData.objects.filter(deviceName=data["deviceName"]).create(deviceName=data["deviceName"], battery=coded_data[0], bin_state=((DeviceSettings.objects.get(deviceName=item.deviceName).bin_height-coded_data[1])*100)/DeviceSettings.objects.get(deviceName=item.deviceName).bin_height, fire=coded_data[2])
            print("Created!")

        else:
            print("Error raised! I guess device that sent data is unknown.")


        all_data = list()
        all_data.append(data["applicationName"])
        all_data.append(data["deviceName"])
        all_data.append(base64.b64decode(data["data"]))
        print(all_data)
        all_data = list()
    return HttpResponse('200')

def test(request):
    context = {}
    context["data"] = DeviceData.objects.all()
    return render(request, "test.html", context)