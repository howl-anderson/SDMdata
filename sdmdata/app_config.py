#!/usr/bin/env python

from datetime import timedelta
from sdmdata.db_config import DATABASE_URI

DEBUG = True
SECRET_KEY = 's2ek42dwo4k2dw'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
REMEMBER_COOKIE_DURATION = timedelta(days=30)