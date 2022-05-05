python manage.py makemigrations && python manage.py migrate
gunicorn --bind 0:8040 waitinghow.wsgi
