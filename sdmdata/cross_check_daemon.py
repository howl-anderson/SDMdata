#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import multiprocessing

from lib.worker_daemon import Daemon

cpu_core_count = multiprocessing.cpu_count()

if cpu_core_count is None:
    multiprocess_flag = False
elif cpu_core_count < 4:
    # If cpu core less than 4, we don't do multiprocess
    multiprocess_flag = False
else:
    multiprocess_flag = True

if multiprocess_flag:
    from lib.cross_check_multiprocess import cross_check
else:
    from lib.cross_check_main import cross_check


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
