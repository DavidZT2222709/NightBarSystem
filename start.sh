#!/bin/sh
echo "==> Running migrations..."
python backend/manage.py migrate --noinput
echo "==> Running collectstatic..."
python backend/manage.py collectstatic --noinput
echo "==> Starting gunicorn..."
exec gunicorn config.wsgi:application --chdir backend --bind 0.0.0.0:$PORT
