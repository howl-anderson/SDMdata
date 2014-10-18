#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
from sdmdata.worker_daemon import Daemon
#from sdmdata.cross_check_main import cross_check
from sdmdata.cross_check_mutilprocess import cross_check


class MyDaemon(Daemon):
    def __init__(self, work_path, daemon_name):
        Daemon.__init__(self, work_path, daemon_name)

    def _run(self):
        cross_check(self.work_path)
        sys.exit(0)


if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])
    current_path = os.path.abspath(pathname)
    daemon = MyDaemon(current_path, "cross_check")
    daemon.handle_argument()