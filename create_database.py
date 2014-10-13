#!/usr/bin/env python

# import build-in library
from argparse import ArgumentParser

from sdmdata.sdmdata.db import create_connect


parser = ArgumentParser(description="Create SDMdata database")
parser.add_argument("database", default="sdmdata", help="Database for SDMdata, default name is 'sdmdata'", nargs="?")
args = parser.parse_args()

db_name = args.database
db_connect = create_connect()
db_connect.execute("commit")
db_connect.execute("create database %s" % db_name)
db_connect.close()
