pkill uwsgi
python manage.py makemigrations
python manage.py migrate
# nohup python manage.py runserver 0.0.0.0:8000 &
systemctl start nginx.service
uwsgi --ini uwsgi.ini 
