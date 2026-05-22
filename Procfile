web: gunicorn config.wsgi:application --chdir backend --bind 0.0.0.0:$PORT
release: python backend/manage.py migrate --noinput && python backend/manage.py collectstatic --noinput --clear
