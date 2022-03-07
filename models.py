# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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
