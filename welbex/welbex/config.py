# -*- coding: utf-8 -*-
# configuration file
# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import os
import sys

# ---------------------------------------------------------------------------------------------------------------------
# CONFIGURATION

# DATABASE
DATABASE_INFO = {'database': 'jangodb', 'host': 'dino-server', 'user': 'django',
                 'password': 'postgres', 'port': 5432}

# project path
path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
