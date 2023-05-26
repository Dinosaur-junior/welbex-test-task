import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Cargo(models.Model):
    pick_up_location = models.IntegerField(verbose_name='Pick-up')
    delivery_location = models.IntegerField(verbose_name='Delivery')
    weight = models.IntegerField(verbose_name='Вес', validators=[MaxValueValidator(1000), MinValueValidator(1)])
    description = models.TextField(verbose_name='Описание')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'


def check_car_number(value):
    if not bool(re.match(r"[1000-9999]+[A-Z]", value)):
        raise ValidationError(f"{value} - invalid car number")


class Car(models.Model):
    number = models.CharField(unique=True, max_length=5, validators=[check_car_number, ], verbose_name='Номер')
    location = models.IntegerField(verbose_name='Локация')
    weight = models.IntegerField(verbose_name='Грузоподъемность',
                                 validators=[MaxValueValidator(1000), MinValueValidator(1)])
    objects = models.Manager()

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Location(models.Model):
    city = models.CharField(max_length=255, verbose_name='Город')
    state = models.CharField(max_length=255, verbose_name='Штат')
    postal_code = models.IntegerField(verbose_name='Почтовый индекс')
    latitude = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='Долгота')
    objects = models.Manager()

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
