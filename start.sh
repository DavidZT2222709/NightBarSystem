#!/bin/sh
python backend/manage.py migrate --noinput
python backend/manage.py collectstatic --noinput
exec gunicorn config.wsgi:application --chdir backend --bind 0.0.0.0:$PORT
