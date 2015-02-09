#!/bin/bash

sudo apt-get update
sudo apt-get --yes install libgdal-dev python-setuptools libpython-dev python-pip python-mysqldb python-gdal python-yaml

sudo pip install tablib flask flask-login sqlalchemy iso3166 gunicorn psutil
