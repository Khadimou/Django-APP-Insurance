from django.db import models

# Create your models here.
class Vehicle(models.Model):
    VEHICLE_TYPE = models.CharField(max_length=40)
    VEHICLE_YEAR = models.IntegerField()
    AGE = models.IntegerField()
    DRIVING_EXPERIENCE = models.IntegerField()
    SPEEDING_VIOLATIONS = models.IntegerField()
    DUIS = models.IntegerField()
    VEHICLE_OWNERSHIP = models.BooleanField()
    PAST_ACCIDENTS = models.IntegerField()

class Info(models.Model):
    CIVILITY = models.CharField(max_length=40)
    FIRST_NAME = models.CharField(max_length=40)
    LAST_NAME = models.CharField(max_length=40) 
    EMAIL = models.CharField(max_length=40)
    DRIVING_EXPERIENCE = models.IntegerField()
    CAR_OWNERSHIP = models.BooleanField()
    CLAIMS = models.BooleanField()