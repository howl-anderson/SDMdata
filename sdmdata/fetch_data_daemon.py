#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
from sdmdata.worker_daemon import Daemon
from sdmdata.collect_record_main import collect_record_data


class MyDaemon(Daemon):
    def __init__(self, work_path, daemon_name):
        Daemon.__init__(self, work_path, daemon_name)

    def _run(self):
        # TODO: need log function
        collect_record_data(self.work_path)
        sys.exit(0)


if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])
    current_path = os.path.abspath(pathname)
    daemon = MyDaemon(current_path, "fetch_occurrence")
    daemon.handle_argument()