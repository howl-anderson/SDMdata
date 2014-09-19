#!/usr/bin/env python
#-*-coding:utf-8-*-

import os
import sys
import subprocess

subdir_list = os.listdir(".")

for subdir in subdir_list:
    subdir = os.path.join(".", subdir)
    print(subdir)
    # continue
    subprocess.Popen("cd %s; rm *_adm1.*; rm *_adm2.*; rm *_adm3.*; rm *_adm4.*; rm read_me.pdf;" % subdir, shell=True)
