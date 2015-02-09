#!/usr/bin/env python

from datetime import timedelta
import yaml
import os

fp = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../configure/configure.yaml'))
conf = yaml.load(fp)
fp.close()

DEBUG = conf['DEBUG']
SECRET_KEY = conf['SECRET_KEY']

PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)

DATABASE_URI = conf['DATABASE_HOST_URI'] + conf['DATABASE_DATA_URI']
DATABASE_HOST_URI = conf['DATABASE_HOST_URI']