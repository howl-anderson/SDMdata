#!/usr/bin/env python

from datetime import timedelta
from sdmdata.db_config import DATABASE_URI

# DATABASE_URI = 'mysql://root:123456@localhost:3306/sdmdata?charset=utf8'
DEBUG = True
SECRET_KEY = 'foobarbaz'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)
