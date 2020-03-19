from django.db import models


class DeviceData(models.Model):
    id = models.AutoField(primary_key=True)
    deviceName = models.CharField(max_length=255)
    battery = models.FloatField(blank=True, null=True)
    bin_state = models.IntegerField(blank=True, null=True)
    fire = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return "{}".format(self.deviceName)

    class Meta:
        verbose_name = "Device data"
        verbose_name_plural = "Device data"

    def device_icon(self):
        if self.fire:
            return "/static/wasco/images/reddot.png"
        elif self.bin_state>=0 and self.bin_state<25:
            return "/static/wasco/images/green.png"

        elif self.fire:
            return "/static/wasco/images/reddot.png"
        elif self.bin_state>=25 and self.bin_state<50:
            return "/static/wasco/images/yellow.png"

        elif self.fire:
            return "/static/wasco/images/reddot.png"
        elif self.bin_state>=50 and self.bin_state<75:
            return "/static/wasco/images/orange.png"

        elif self.fire:
            return "/static/wasco/images/reddot.png"
        elif self.bin_state>=75:
            return "/static/wasco/images/red.png"

    
    def default(self):
        if self.bin_state>=0 and self.bin_state<25:
            return "/static/wasco/images/green.png"


class DeviceSettings(models.Model):
    id = models.AutoField(primary_key=True)
    deviceName = models.CharField(max_length=255)
    bin_height = models.IntegerField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True) 
    longitude = models.FloatField(blank=True, null=True) 

    def __str__(self):
        return "{} {} {} {}".format(self.deviceName, self.longitude, self.latitude, self.bin_height)

    class Meta:
        verbose_name = "Device location"
        verbose_name_plural = "Device location"



class LogData(models.Model):
    deviceName = models.CharField(max_length=255) 
    battery = models.FloatField(blank=True, null=True)
    bin_state = models.IntegerField(blank=True, null=True)
    fire = models.BooleanField(null=True, blank=True)
    request_time = models.CharField(max_length=255)

    def __str__(self):
        return "{} {}".format(self.deviceName, self.request_time)

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    
class StartPoint(models.Model):
    latitude = models.FloatField(blank=True, null=True) 
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "{} {}".format(self.longitude, self.latitude)

    class Meta:
        verbose_name = "Start point for bins"
        verbose_name_plural = "Start points for bins"