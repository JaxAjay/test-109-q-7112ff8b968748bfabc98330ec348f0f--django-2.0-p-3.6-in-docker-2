# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
def validate_phone(value):
    if len(str(value)) != 10:
        raise ValidationError(('%(value)s is not a 10 digit number'),params={'value': value},)

class DriverRegister(models.Model):
    name = models.CharField(max_length = 200 ,blank = False)
    email = models.EmailField(max_length = 200,blank = False , unique = True)
    phone_number = models.IntegerField(validators=[validate_phone] , blank= False , unique=True)
    license_number = models.CharField(max_length = 200,blank = False , unique = True)
    car_number = models.CharField(max_length = 200,blank = False , unique = True)


class DriverLocation(models.Model):
    driver = models.ForeignKey(DriverRegister , on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return "%s : %s , %s"%(self.driver.name,self.latitude , self.longitude)