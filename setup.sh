python manage.py qcluster

gunicorn fampay.wsgi:application --bind 0.0.0.0:$PORT