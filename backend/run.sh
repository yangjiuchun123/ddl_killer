#./halt.sh
pkill -9 python
#systemctl start nginx.service
rm -rf vue2-forntend/dist
cd vue2-forntend && cnpm run build:prod && cd ..
rm -rf static
# source venv/bin/activate
python manage.py makemigrations
python manage.py collectstatic
python manage.py migrate
 nohup python manage.py runserver 0.0.0.0:8000 &
#nohup uwsgi --ini uwsgi.ini &
