# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
import json
from django.views.decorators.csrf import csrf_exempt
from restapi.models import *
# Create your views here.
from django.forms.models import model_to_dict
from django.shortcuts import  get_object_or_404
import math 

def index(request):
    # for database cleaning

    # DriverLocation.objects.all().delete()
    # DriverRegister.objects.all().delete()
    
    return HttpResponse("Hello, world. You're at Rest.")

@csrf_exempt
def driverRegister(request):
    if  'application/json' not in request.content_type :
        return HttpResponse(json.dumps({'message' : 'content type json only'}), content_type='application/json', status = 402)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            obj = DriverRegister(**data)
            obj.full_clean()
            obj.save()
        except Exception as e:
            if type(e) == type(ValidationError("test")):
                e = ", ".join([ "%s : %s"%(k,j) for k,v in e.message_dict.items() for j in v])
            return HttpResponse(json.dumps({'status':"failure" , 'reason' : str(e)}), content_type='application/json', status = 400)
        return HttpResponse(json.dumps(model_to_dict(obj , fields=[field.name for field in obj._meta.fields])) , content_type='application/json', status = 201)
    else :
        return HttpResponse(json.dumps({'message' : 'method not allowed!'}), content_type='application/json', status = 405)

@csrf_exempt
def shareLocation(request , driver_id):
    if  'application/json' not in request.content_type :
        return HttpResponse(json.dumps({'message' : 'content type json only'}), content_type='application/json', status = 402)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            driver_obj = DriverRegister.objects.get(id = driver_id)
            data['driver'] = driver_obj
            loc_obj = DriverLocation(**data)
            loc_obj.full_clean()
            loc_obj.save()
        except Exception as e:
            if type(e) == type(ValidationError("test")):
                e = ", ".join([ "%s : %s"%(k,j) for k,v in e.message_dict.items() for j in v])
            return HttpResponse(json.dumps({'status':"failure" , 'reason' : str(e)}), content_type='application/json', status = 400)
        return HttpResponse(json.dumps({"status": "success"}) , content_type='application/json', status = 202)
    else :
        return HttpResponse(json.dumps({'message' : 'method not allowed!'}), content_type='application/json', status = 405)

def haversine(lat1, lon1, lat2, lon2): 
    # distance between latitudes 
    # and longitudes 
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians 
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
  
    # apply formulae 
    a = (pow(math.sin(dLat / 2), 2) + pow(math.sin(dLon / 2), 2) * math.cos(lat1) * math.cos(lat2)); 
    rad = 6371
    c = 2 * math.asin(math.sqrt(a)) 
    return rad * c

@csrf_exempt
def getCabs(request):
    if  'application/json' not in request.content_type :
        return HttpResponse(json.dumps({'message' : 'content type json only'}), content_type='application/json', status = 402)
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            distance_within_km = 4
            lat = float(data['latitude'])
            lon = float(data['longitude'])
            drivers = DriverRegister.objects.all()
            available_cabs = []
            for driver in drivers:
                d_location = DriverLocation.objects.filter(driver = driver).order_by('-id').first()
                if d_location:
                    distance = haversine(lat , lon , d_location.latitude , d_location.longitude)
                    if distance <= distance_within_km:
                        available_cabs.append({'name' : driver.name , "car_number" : driver.car_number , "phone_number" : driver.phone_number})
            final = {}
            if len(available_cabs):
                final['available_cabs'] = available_cabs
            else:
                final['message'] = "No cabs available!"
        except Exception as e:
            if type(e) == type(ValidationError("test")):
                e = ", ".join([ "%s : %s"%(k,j) for k,v in e.message_dict.items() for j in v])
            return HttpResponse(json.dumps({'status':"failure" , 'reason' : str(e)}), content_type='application/json', status = 400)
        return HttpResponse(json.dumps(final) , content_type='application/json', status = 200)
    else :
        return HttpResponse(json.dumps({'message' : 'method not allowed!'}), content_type='application/json', status = 405)