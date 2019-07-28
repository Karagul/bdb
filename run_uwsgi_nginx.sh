#!/bin/sh
source ~/webdev/bin/activate
uwsgi --ini config/uwsgi.ini #config/uwsgi-single.ini
deactivate
