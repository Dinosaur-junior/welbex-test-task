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
import os

from django.core.asgi import get_asgi_application

# ---------------------------------------------------------------------------------------------------------------------
# ASGI configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welbex.settings')

application = get_asgi_application()
