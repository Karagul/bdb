#!/bin/bash
source ~/webdev/bin/activate
uwsgi --ini config/uwsgi.ini #config/uwsgi-single.ini
deactivate
echo 'Venv deactivated'
