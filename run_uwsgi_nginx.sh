#!/bin/bash
sudo service postgresql start
sudo service nginx start
source ~/webdev/bin/activate
uwsgi --ini config/uwsgi.ini

deactivate
echo 'Venv deactivated'
sudo service postgresql stop
sudo service nginx stop
echo 'PG and nginx services stopped'
