#!/usr/bin/env python

import hashlib

from sdmdata.sdmdata.db import create_session
from sdmdata.sdmdata.db import User

username = "admin"
password = "admin"
hash_obj = hashlib.md5()
hash_obj.update(password)
hashed_password = hash_obj.hexdigest()
db_session = create_session()
user_flag = db_session.query(User).filter(User.login_name == "admin").count()
if user_flag:
    print "admin already exists! Nothing change!"
else:
    user = User(login_name=username, password=hashed_password)
    db_session.add(user)
    db_session.commit()
    print "Admin account is created! Password: admin"