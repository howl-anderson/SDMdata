#!/usr/bin/env python
# -*- coding:utf-8 -*-

# import build-in library
import hashlib
from argparse import ArgumentParser

from sdmdata.lib.db import create_session
from sdmdata.lib.db import User


parser = ArgumentParser(description="Create admin account")
parser.add_argument("password",
                    default="admin",
                    help="Password for admin, default password is 'admin'",
                    nargs="?")
args = parser.parse_args()

username = "admin"
password = args.password
hash_obj = hashlib.md5()
hash_obj.update(password)
hashed_password = hash_obj.hexdigest()
db_session = create_session()
user_flag = db_session.query(User).filter(User.login_name == "admin").count()
if user_flag:
    print "Admin account already exists! Nothing change!"
else:
    user = User(login_name=username, password=hashed_password)
    db_session.add(user)
    db_session.commit()
    print "Admin account is created! Password: admin"
