#!/usr/bin/env python

from setuptools import setup

setup(
    name='sdmdata',
    version='0.1',
    long_description=__doc__,
    packages=['sdmdata'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
    'Flask>=0.9',
    'SQLAlchemy>=0.6',
    'iso3166',
    'requests',
    'gunicorn',
    'tablib',
    "flask-login",
    "click",
    "chardet"
    ]
)
