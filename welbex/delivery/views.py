import operator

from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import LocationForm, CargoForm, CarForm, SearchForm
from .models import Cargo, Location, Car, check_car_number


# Create your views here.

# index page
def index(request):
    return render(request, 'delivery/index.html', {'cargo_search_form': SearchForm(initial={'object_type': 'cargo'}),
                                                   'car_search_form': SearchForm(initial={'object_type': 'car'}),
                                                   'location_search_form':
                                                       SearchForm(initial={'object_type': 'location'}), })


def search(request):
    if request.method == 'GET':
        return redirect('/')
    elif request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            if form.data['object_type'] == 'cargo':
                if form.data['query'].isdigit():
                    cargo_obj = Cargo.objects.filter(pk=int(form.data['query']))
                    if len(cargo_obj) == 0:
                        form.add_error(None, 'Груз с таким ID не найден')
                    else:
                        return redirect(f'/cargo_info/{form.data["query"]}')

                else:
                    form.add_error(None, 'Вы ввели не число')
                return render(request, 'delivery/index.html',
                              {'cargo_search_form': form,
                               'car_search_form': SearchForm(initial={'object_type': 'car'}),
                               'location_search_form':
                                   SearchForm(initial={'object_type': 'location'}), })

            elif form.data['object_type'] == 'car':
                if form.data['query'].isdigit():
                    car_obj =Car.objects.filter(pk=int(form.data['query']))
                    if len(car_obj) == 0:
                        form.add_error(None, 'Машина с таким ID не найдена')
                    else:
                        return redirect(f'/car_info/{car_obj[0].pk}')

                else:
                    car_obj = Car.objects.filter(number=form.data['query'])
                    if len(car_obj) == 0:
                        form.add_error(None, 'Машина с таким номером не найдена')
                    else:
                        return redirect(f'/car_info/{car_obj[0].pk}')
                return render(request, 'delivery/index.html',
                              {'cargo_search_form': SearchForm(initial={'object_type': 'cargo'}),
                               'car_search_form': SearchForm(initial={'object_type': 'car'}),
                               'location_search_form': form, })

            elif form.data['object_type'] == 'location':
                if form.data['query'].isdigit():
                    location_obj = Location.objects.filter(postal_code=int(form.data['query']))
                    if len(location_obj) == 0:
                        form.add_error(None, 'Локация с таким индексом не найдена')
                    else:
                        return redirect(f'/location_info/{location_obj[0].pk}')

                else:
                    form.add_error(None, 'Вы ввели не число')
                return render(request, 'delivery/index.html',
                              {'cargo_search_form': SearchForm(initial={'object_type': 'cargo'}),
                               'car_search_form': SearchForm(initial={'object_type': 'car'}),
                               'location_search_form': form, })
            else:
                messages.error(request, f'Несуществующий объект')
                return redirect('/')
        else:
            form.add_error(None, 'Некорректный ввод')
        return render(request, 'delivery/index.html', {'cargo_search_form': form,
                                                       'car_search_form': form,
                                                       'location_search_form': form, })


def cargo(request):
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


def cargo_info(request, cargo_id):
    cargo_obj = Cargo.objects.get(pk=cargo_id)
    form = CargoForm(instance=cargo_obj)
    return render(request, 'delivery/cargo_page.html', {'cargo': cargo_obj, 'form': form})


def edit_cargo(request, cargo_id):
    cargo_object = Cargo.objects.get(pk=cargo_id)
    if request.method == 'GET':
        form = CargoForm(instance=cargo_object)
        return render(request, 'admin_panel/cargo_page.html', {'form': form, 'cargo': cargo_object})
    elif request.method == 'POST':
        form = CargoForm(request.POST, instance=cargo_object)
        if form.is_valid():
            form.save()
            return redirect(f'/cargo_info/{cargo_id}')
        return render(request, 'admin_panel/cargo_page.html', {'form': form, 'cargo': cargo_object})


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


def car_info(request, car_id):
    car_obj = Car.objects.get(pk=car_id)
    form = CarForm(instance=car_obj)
    return render(request, 'delivery/car_page.html', {'car': car_obj, 'form': form})


def edit_car(request, car_id):
    car_object = Car.objects.get(pk=car_id)
    if request.method == 'GET':
        form = CarForm(instance=car_object)
        return render(request, 'admin_panel/car_page.html', {'form': form, 'car': car_object})
    elif request.method == 'POST':
        form = CarForm(request.POST, instance=car_object)
        if form.is_valid():
            form.save()
            return redirect(f'/car_info/{car_id}')
        return render(request, 'admin_panel/car_page.html', {'form': form, 'car': car_object})


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


def location_info(request, location_id):
    location_obj = Location.objects.get(pk=location_id)
    form = LocationForm(instance=location_obj)
    return render(request, 'delivery/location_page.html', {'location': location_obj, 'form': form})


def edit_location(request, location_id):
    location_object = Location.objects.get(pk=location_id)
    if request.method == 'GET':
        form = LocationForm(instance=location_object)
        return render(request, 'admin_panel/location_page.html', {'form': form, 'location': location_object})
    elif request.method == 'POST':
        form = LocationForm(request.POST, instance=location_object)
        if form.is_valid():
            form.save()
            return redirect(f'/location_info/{location_id}')
        return render(request, 'admin_panel/location_page.html', {'form': form, 'location': location_object})
