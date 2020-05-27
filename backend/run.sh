for i in `ps -ef|grep uwsgi |awk '{print $2}' `; do kill -9 $i ; done;
rm -rf vue2-forntend/dist
cd vue2-forntend && cnpm run build:prod && cd ..
rm -rf static
python manage.py makemigrations
python manage.py collectstatic
python manage.py migrate
#python manage.py runserver 0.0.0.0:8000 
uwsgi --ini uwsgi.ini 
