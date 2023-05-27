import operator

from django.shortcuts import render, redirect

from .forms import LocationForm, CargoForm, CarForm
from .models import Cargo, Location, Car, check_car_number
from geopy.distance import geodesic as GD


# Create your views here.

# index page
def index(request):
    return render(request, 'delivery/index.html')


def cargo(request):
    all_cars = Car.objects.all()
    cargo_list = Cargo.objects.all()
    cargo_list = sorted(cargo_list, key=operator.attrgetter('pk'))

    return render(request, 'delivery/cargo.html', {'cargos': cargo_list, 'form': CargoForm})


def new_cargo(request):
    form = CargoForm(request.POST)
    if form.is_valid():
        loc1 = Location.objects.filter(postal_code=form.data['pick_up_location'])
        loc2 = Location.objects.filter(postal_code=form.data['delivery_location'])
        if len(loc1) > 0 and len(loc2) > 0 and form.data['pick_up_location'] != form.data['delivery_location']:
            form.save()
            return redirect('cargo_main')

        else:
            form.add_error(None, 'Некорректные локации')
            cargo_list = Cargo.objects.all()
            return render(request, 'delivery/cargo.html', {'cargos': cargo_list, 'form': form})
    else:
        cargo_list = Cargo.objects.all()
        cargo_list = sorted(cargo_list, key=operator.attrgetter('pk'))
        return render(request, 'delivery/cargo.html', {'cargos': cargo_list, 'form': form})


def delete_cargo(request, cargo_id):
    loc = Cargo.objects.get(pk=cargo_id)
    loc.delete()
    return redirect('cargo_main')


def cars(request):
    cars_list = Car.objects.all()
    cars_list = sorted(cars_list, key=operator.attrgetter('number'))
    return render(request, 'delivery/cars.html', {'cars': cars_list, 'form': CarForm})


def new_car(request):
    form = CarForm(request.POST)
    if form.is_valid():
        loc = Location.objects.filter(postal_code=form.data['location'])
        flag = True
        if len(loc) == 0:
            form.add_error(None, 'Некорректная локации')
            flag = False

        if not check_car_number(form.data['number']):
            form.add_error(None, 'Некорректный номер автомобиля')
            flag = False

        if flag:
            form.save()
            return redirect('cars_main')

        else:
            cars_list = Car.objects.all()
            cars_list = sorted(cars_list, key=operator.attrgetter('number'))
            return render(request, 'delivery/cars.html', {'cars': cars_list, 'form': form})
    else:
        if 'number' in form.data:
            if not check_car_number(form.data['number']):
                form.add_error(None, 'Некорректный номер автомобиля')

        cars_list = Car.objects.all()
        cars_list = sorted(cars_list, key=operator.attrgetter('number'))
        return render(request, 'delivery/cars.html', {'cars': cars_list, 'form': form})


def delete_car(request, car_id):
    car = Car.objects.get(pk=car_id)
    car.delete()
    return redirect('cars_main')


def locations(request):
    location_list = Location.objects.all()
    location_list = sorted(location_list, key=operator.attrgetter('postal_code'))
    return render(request, 'delivery/locations.html', {'locations': location_list, 'form': LocationForm})


def new_location(request):
    form = LocationForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('locations_main')
    else:
        location_list = Location.objects.all()
        location_list = sorted(location_list, key=operator.attrgetter('postal_code'))
        return render(request, 'delivery/locations.html', {'locations': location_list, 'form': form})


def delete_location(request, location_id):
    loc = Location.objects.get(pk=location_id)
    loc.delete()
    return redirect('locations_main')
