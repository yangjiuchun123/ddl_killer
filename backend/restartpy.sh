pkill uwsgi
python manage.py makemigrations
python manage.py migrate
# nohup python manage.py runserver 0.0.0.0:8000 &
uwsgi --ini uwsgi.ini 
