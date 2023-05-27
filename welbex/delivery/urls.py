from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='delivery_main'),
    path('search', search, name='search'),

    path('cargo', cargo, name='cargo_main'),
    path('new_cargo', new_cargo, name='new_cargo'),
    path('delete_cargo/<int:cargo_id>/', delete_cargo, name='delete_cargo'),
    path('cargo_info/<int:cargo_id>/', cargo_info, name='cargo_info'),
    path('edit_cargo/<int:cargo_id>/', edit_cargo, name='edit_cargo'),

    path('cars', cars, name='cars_main'),
    path('new_car', new_car, name='new_car'),
    path('delete_car/<int:car_id>/', delete_car, name='delete_car'),
    path('car_info/<int:car_id>/', car_info, name='car_info'),
    path('edit_car/<int:car_id>/', edit_car, name='edit_car'),

    path('locations', locations, name='locations_main'),
    path('new_location', new_location, name='new_location'),
    path('delete_location/<int:location_id>/', delete_location, name='delete_location'),
    path('location_info/<int:location_id>/', location_info, name='location_info'),
    path('edit_location/<int:location_id>/', edit_location, name='edit_location'),

]
