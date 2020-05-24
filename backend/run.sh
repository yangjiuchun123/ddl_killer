./halt.sh
# pkill -9 python
systemctl start nginx.service
rm -rf vue2-forntend/dist
cd vue2-forntend && cnpm run build:prod && cd ..
rm -rf static
#source venv/bin/activate
python manage.py makemigrations
python manage.py collectstatic
python manage.py migrate
#python manage.py runserver 0.0.0.0:8000 
uwsgi --ini uwsgi.ini 
