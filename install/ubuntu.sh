#!/bin/bash

sudo apt-get update
sudo apt-get install libgdal-dev python-setuptools libpython-dev python-pip python-mysqldb python-gdal

sudo pip install tablib flask flask-login sqlalchemy iso3166 gunicorn
