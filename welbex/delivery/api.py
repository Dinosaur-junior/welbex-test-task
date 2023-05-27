# -*- coding: utf-8 -*-
# Written by Dinosaur
#                __
#               / _)
#      _.----._/ /
#     /         /
#  __/ (  | (  |
# /__.-'|_|--|_|


# ---------------------------------------------------------------------------------------------------------------------
# import libraries

import operator

from django.http import JsonResponse
from django.shortcuts import redirect

from .forms import LocationForm, CargoForm, CarForm, SearchForm
from .models import Cargo, Location, Car, check_car_number


# ---------------------------------------------------------------------------------------------------------------------
# API methods

# SEARCH
def api_search(request):
    if request.method == 'GET':
        return JsonResponse({'status': 'error', 'errors': ['Необходимо выполнить POST запрос']})

    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():

            # search for cargo
            if form.data['object_type'] == 'cargo':
                if form.data['query'].isdigit():
                    cargo_obj = Cargo.objects.filter(pk=int(form.data['query']))
                    if len(cargo_obj) == 0:
                        return JsonResponse({'status': 'error', 'errors': ['Груз не найден']})
                    else:
                        return redirect(f'/api/cargo_info/{form.data["query"]}')

                else:
                    return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})

            # search for car
            elif form.data['object_type'] == 'car':
                if form.data['query'].isdigit():
                    car_obj = Car.objects.filter(pk=int(form.data['query']))
                    if len(car_obj) == 0:
                        return JsonResponse({'status': 'error', 'errors': ['Машина не найдена']})
                    else:
                        return redirect(f'/api/car_info/{car_obj[0].pk}')

                else:
                    car_obj = Car.objects.filter(number=form.data['query'])
                    if len(car_obj) == 0:
                        return JsonResponse({'status': 'error', 'errors': ['Машина не найдена']})
                    else:
                        return redirect(f'/api/car_info/{car_obj[0].pk}')

            # search for location
            elif form.data['object_type'] == 'location':
                if form.data['query'].isdigit():
                    location_obj = Location.objects.filter(postal_code=int(form.data['query']))
                    if len(location_obj) == 0:
                        location_obj = Location.objects.filter(pk=int(form.data['query']))
                        if len(location_obj) == 0:
                            return JsonResponse({'status': 'error', 'errors': ['Локация не найдена']})
                        else:
                            return redirect(f'api/location_info/{location_obj[0].pk}')
                    else:
                        return redirect(f'api/location_info/{location_obj[0].pk}')

                else:
                    return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})

            # unknown object
            else:
                return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})
        else:
            return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})


# ---------------------------------------------------------------------------------------------------------------------
# CARGO

# get list of cargos
def api_cargo(request):
    cargo_list = Cargo.objects.all()
    cargo_list = sorted(cargo_list, key=operator.attrgetter('pk'))
    cargo_info = {i.pk: {'pick-up': i.pick_up_location,
                         'delivery': i.delivery_location,
                         'wight': i.weight,
                         'description': i.description,
                         'nearest_cars': i.get_cars(), } for i in cargo_list}
    cargo_info['status'] = 'success'
    cargo_info['errors'] = []
    return JsonResponse(cargo_info)


# add cargo
def api_new_cargo(request):
    form = CargoForm(request.POST)
    if form.is_valid():
        loc1 = Location.objects.filter(postal_code=form.data['pick_up_location'])
        loc2 = Location.objects.filter(postal_code=form.data['delivery_location'])
        if len(loc1) > 0 and len(loc2) > 0 and form.data['pick_up_location'] != form.data['delivery_location']:
            form.save()
            return JsonResponse({'status': 'success', 'errors': []})

        else:
            return JsonResponse({'status': 'error', 'errors': ['Некорректные локации']})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})


# delete cargo by id
def api_delete_cargo(request, cargo_id):
    cargo = Cargo.objects.filter(pk=cargo_id)
    if len(cargo) > 0:
        cargo[0].delete()
        return JsonResponse({'status': 'success', 'errors': []})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Груз не найден']})


# get cargos info by id
def api_cargo_info(request, cargo_id):
    cargo_obj = Cargo.objects.filter(pk=cargo_id)
    if len(cargo_obj) == 0:
        return JsonResponse({'status': 'error', 'errors': ['Груз не найден']})
    else:
        cargo_obj = cargo_obj[0]
        return JsonResponse({'id': cargo_obj.pk,
                             'pick-up': cargo_obj.pick_up_location,
                             'delivery': cargo_obj.delivery_location,
                             'weight': cargo_obj.weight,
                             'description': cargo_obj.description,
                             'nearest_cars': cargo_obj.get_cars(),
                             'status': 'error',
                             'errors': []})


# edit cargo by id
def api_edit_cargo(request, cargo_id):
    cargo_object = Cargo.objects.filter(pk=cargo_id)
    if len(cargo_object) == 0:
        return JsonResponse({'status': 'error', 'errors': ['Груз не найден']})
    else:
        cargo_object = cargo_object[0]
        form = request.POST
        flag = False

        if 'weight' in form:
            if form['weight'].isdigit():
                cargo_object.weight = form['weight']
                cargo_object.save()
                flag = True
            else:
                flag = False

        if 'description' in form:
            cargo_object.description = form['description']
            cargo_object.save()
            flag = True

        if flag:
            return JsonResponse({'status': 'success', 'errors': []})
        else:
            return JsonResponse({'status': 'error', 'errors': ['Неккоректые данные']})


# ---------------------------------------------------------------------------------------------------------------------
# CARS

# get list of all cars
def api_cars(request):
    cars_list = Car.objects.all()
    cars_list = sorted(cars_list, key=operator.attrgetter('number'))
    cars_info = {i.pk: {'number': i.pick_up_location,
                        'location': i.delivery_location,
                        'weight': i.weight} for i in cars_list}
    cars_info['status'] = 'success'
    cars_info['errors'] = []
    return JsonResponse(cars_info)


# add car
def api_new_car(request):
    form = CarForm(request.POST)
    if form.is_valid():
        loc = Location.objects.filter(postal_code=form.data['location'])
        if len(loc) == 0:
            return JsonResponse({'status': 'error', 'errors': ['Некорректная локация']})

        if not check_car_number(form.data['number']):
            return JsonResponse({'status': 'error', 'errors': ['Некорректный номер машины']})

        form.save()
        return JsonResponse({'status': 'success', 'errors': []})

    else:
        return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})


# # delete car by id
def api_delete_car(request, car_id):
    car = Car.objects.filter(pk=car_id)
    if len(car) > 0:
        car[0].delete()
        return JsonResponse({'status': 'success', 'errors': []})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Машина не найдена']})


# get cars info by id
def api_car_info(request, car_id):
    car = Car.objects.filter(pk=car_id)
    if len(car) > 0:
        return JsonResponse({'id': car.pk,
                             'number': car.number,
                             'location': car.location,
                             'weight': car.weight,
                             'status': 'success', 'errors': []})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Машина не найдена']})


# edit car by id
def api_edit_car(request, car_id):
    car = Car.objects.filter(pk=car_id)
    if len(car) > 0:
        car = car[0]
        form = request.POST
        flag = False

        if 'location' in form and form['location'].isdigit():
            loc = Location.objects.filter(postal_code=form.data['location'])
            if len(loc) == 0:
                return JsonResponse({'status': 'error', 'errors': ['Некорректная локация']})
            else:
                car.location = loc.pk
                car.save()
                flag = True

        if 'weight' in form and form['weight'].isdigit():
            car.weight = form['weight']
            car.save()
            flag = True

        if flag:
            return JsonResponse({'status': 'success', 'errors': []})
        else:
            return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})

    else:
        return JsonResponse({'status': 'error', 'errors': ['Машина не найдена']})


# ---------------------------------------------------------------------------------------------------------------------
# LOCATIONS

# get all locations list
def api_locations(request):
    location_list = Location.objects.all()
    location_list = sorted(location_list, key=operator.attrgetter('postal_code'))
    locations_info = {i.pk: {'postal_code': i.postal_code,
                             'city': i.city,
                             'state': i.state,
                             'latitude': i.latitude,
                             'longitude': i.longitude} for i in location_list}
    locations_info['status'] = 'success'
    locations_info['errors'] = []
    return JsonResponse(locations_info)


# add location
def api_new_location(request):
    form = LocationForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success', 'errors': []})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})


# delete location by id
def api_delete_location(request, location_id):
    loc = Location.objects.filter(pk=location_id)
    if len(loc) > 0:
        loc[0].delete()
        return JsonResponse({'status': 'success', 'errors': []})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Локация не найдена']})


# get locations info by id
def api_location_info(request, location_id):
    location_obj = Location.objects.filter(pk=location_id)
    if len(location_obj) > 0:
        loc = location_obj[0]
        return JsonResponse({'id': loc.pk,
                             'postal_code': loc.postal_code,
                             'city': loc.city,
                             'state': loc.state,
                             'latitude': loc.latitude,
                             'longitude': loc.longitude, 'status': 'success', 'errors': []})
    else:
        return JsonResponse({'status': 'error', 'errors': ['Локация не найдена']})


# edit location by id
def api_edit_location(request, location_id):
    location_object = Location.objects.filter(pk=location_id)
    if len(location_object) > 0:
        form = request.POST
        loc = location_object[0]
        flag = False

        if 'city' in form:
            loc.city = form['city']
            loc.save()
            flag = True

        if 'state' in form:
            loc.state = form['state']
            loc.save()
            flag = True

        if 'postal_code' in form and form['postal_code'].isdigit():
            location_object = Location.objects.filter(postal_code=form['postal_code'])
            if len(location_object) > 0:
                return JsonResponse({'status': 'error', 'errors': ['Локация с таким почтовым индексом уже существует']})
            else:
                loc.postal_code = form['postal_code']
                loc.save()
                flag = True

        if 'latitude' in form and form['latitude'].isdecimal():
            loc.latitude = form['latitude']
            loc.save()
            flag = True

        if 'longitude' in form and form['longitude'].isdecimal():
            loc.longitude = form['longitude']
            loc.save()
            flag = True

        if flag:
            return JsonResponse({'status': 'success', 'errors': []})
        else:
            return JsonResponse({'status': 'error', 'errors': ['Некорректные данные']})

    else:
        return JsonResponse({'status': 'error', 'errors': ['Локация не найдена']})
