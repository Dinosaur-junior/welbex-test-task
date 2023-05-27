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

from django.core.wsgi import get_wsgi_application

# ---------------------------------------------------------------------------------------------------------------------
# WSGI configuration

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welbex.settings')

application = get_wsgi_application()
