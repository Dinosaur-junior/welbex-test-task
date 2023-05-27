import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from geopy.distance import geodesic


class Cargo(models.Model):
    pick_up_location = models.IntegerField(verbose_name='Pick-up')
    delivery_location = models.IntegerField(verbose_name='Delivery')
    weight = models.IntegerField(verbose_name='Вес', validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField(verbose_name='Описание')
    objects = models.Manager()

    def get_cars(self):
        cars = Car.objects.all()
        locs = [self.pick_up_location]
        [locs.append(i.location) for i in cars]
        all_locs = Location.objects.filter(postal_code__in=locs)
        all_locs = {i.postal_code: (i.latitude, i.longitude) for i in all_locs}
        distances = {car.pk: geodesic(all_locs[self.pick_up_location], all_locs[car.location]).miles for car in cars if
                     car.weight >= self.weight}
        return distances

    def get_cars_info(self):
        cars = Car.objects.all()
        cars = {i.pk: i.number for i in cars}
        cars_info = self.get_cars()
        cars_info = {i: [cars[i], f'{round(cars_info[i], 2)} миль'] for i in cars_info}
        info = ''
        for i in cars_info:
            info += f'{cars_info[i][0]}: {cars_info[i][1]}\n'
        return info

    def get_nearest_cars_amount(self):
        cars = self.get_cars()
        cars = {i: cars[i] for i in cars if cars[i] <= 450}
        return len(cars)

    def get_absolute_url(self):
        return reverse('cargo_info', kwargs={'cargo_id': self.pk})

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'


def car_number_validator(value):
    if not check_car_number(value):
        raise ValidationError(f"{value} - invalid car number")


def check_car_number(value):
    return bool(re.match(r"[1000-9999]+[A-Z]", value))


class Car(models.Model):
    number = models.CharField(unique=True, max_length=5, validators=[car_number_validator, ], verbose_name='Номер')
    location = models.IntegerField(verbose_name='Локация')
    weight = models.IntegerField(verbose_name='Грузоподъемность',
                                 validators=[MaxValueValidator(1000), MinValueValidator(1)])
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('car_info', kwargs={'car_id': self.pk})

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Location(models.Model):
    city = models.CharField(max_length=255, verbose_name='Город')
    state = models.CharField(max_length=255, verbose_name='Штат')
    postal_code = models.IntegerField(verbose_name='Почтовый индекс', unique=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='Долгота')
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('location_info', kwargs={'location_id': self.pk})

    class Meta:
        verbose_name = 'Локации'
        verbose_name_plural = 'Локации'
