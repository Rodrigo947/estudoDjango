#!/bin/sh
python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py runserver 0.0.0.0:$DJANGO_PORT_INSIDE