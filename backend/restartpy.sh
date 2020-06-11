pkill python
for i in `ps -ef|grep uwsgi |awk '{print $2}' `; do kill -9 $i ; done;
python manage.py makemigrations
python manage.py migrate
# nohup python manage.py runserver 0.0.0.0:8000 &
systemctl start nginx.service
uwsgi --ini uwsgi.ini 
