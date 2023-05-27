#!/usr/bin/env python
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
import sys


# ---------------------------------------------------------------------------------------------------------------------
# main function
def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'welbex.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


# ---------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
