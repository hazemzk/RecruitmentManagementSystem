python manage.py migrate
gunicorn recruitment_system.wsgi:application --bind 0.0.0.0:10000
