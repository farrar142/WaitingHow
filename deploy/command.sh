python3 manage.py makemigrations && python3 manage.py migrate
echo yes|python3 manage.py collectstatic
gunicorn --bind 0:8040 waitinghow.wsgi
