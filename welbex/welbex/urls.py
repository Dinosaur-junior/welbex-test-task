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
from django.contrib import admin
from django.urls import path, include

# ---------------------------------------------------------------------------------------------------------------------
# URL patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('delivery.urls')),
]
