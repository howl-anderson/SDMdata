#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
from lib.worker_daemon import Daemon
from lib.check_species_main import check_species_data


class MyDaemon(Daemon):
    def __init__(self, work_path, daemon_name):
        Daemon.__init__(self, work_path, daemon_name)

    def _run(self):
        check_species_data()
        sys.exit(0)


if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])
    current_path = os.path.abspath(pathname)
    daemon = MyDaemon(current_path, "check_species_name_daemon")
    daemon.handle_argument()