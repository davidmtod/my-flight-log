from django.db import models
from django.forms import ModelForm


class Logbook(models.Model):
    log_id = models.AutoField(primary_key=True)
    date_of_flight = models.DateField(blank=True, null=True)
    aircraft_type = models.CharField(max_length=40, blank=True, null=True)
    registration = models.CharField(max_length=12, blank=True, null=True)
    captain = models.CharField(max_length=40, blank=True, null=True)
    holder_operating_capacity = models.CharField(max_length=12, blank=True, null=True)
    airfield_from = models.CharField(max_length=40, blank=True, null=True)
    airfield_to = models.CharField(max_length=40, blank=True, null=True)
    depart_gmt = models.DateTimeField(blank=True, null=True)
    arrive_gmt = models.DateTimeField(blank=True, null=True)
    total_time = models.TimeField(blank=True, null=True)
    p1_se_day = models.TimeField(blank=True, null=True)
    dual_se_day = models.TimeField(blank=True, null=True)
    p1_me_day = models.TimeField(blank=True, null=True)
    dual_me_day = models.TimeField(blank=True, null=True)
    p1_se_night = models.TimeField(blank=True, null=True)
    dual_se_night = models.TimeField(blank=True, null=True)
    p1_me_night = models.TimeField(blank=True, null=True)
    dual_me_night = models.TimeField(blank=True, null=True)
    instrument_flying = models.TimeField(blank=True, null=True)
    simulated_instrument_flying = models.TimeField(blank=True, null=True)
    takeoff_day = models.IntegerField(blank=True, null=True)
    landing_day = models.IntegerField(blank=True, null=True)
    takeoff_night = models.IntegerField(blank=True, null=True)
    landing_night = models.IntegerField(blank=True, null=True)
    takeoff_water = models.IntegerField(blank=True, null=True)
    landing_water = models.IntegerField(blank=True, null=True)
    remarks = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logbook'

class LogbookForm(ModelForm):
	class Meta:
		model = Logbook
		fields = '__all__' 

