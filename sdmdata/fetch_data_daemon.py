#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import os
from sdmdata.worker_daemon import Daemon
from sdmdata.collect_record_main import collect_record_data


class MyDaemon(Daemon):
    def __init__(self, work_path, daemon_name):
        self.work_path = work_path
        Daemon.__init__(self, pidfile=os.path.join(work_path, daemon_name + "_daemon.pid"),
                        stderr=os.path.join(work_path, daemon_name + '_daemon_err.log'),
                        stdout=os.path.join(work_path, daemon_name + '_daemon_out.log'),
                        stdin='/dev/null')
        # task_mgr_log = time.strftime('%Y%m%d') + '.log'
        # self.logger = mod_logger.logger(task_mgr_log)

    def _run(self):
        # self.logger.debug("begin sleep")
        collect_record_data(self.work_path)
        # self.delpid()
        sys.exit(0)
        # self.logger.debug("end sleep")


if __name__ == "__main__":
    pathname = os.path.dirname(sys.argv[0])
    work_path = os.path.abspath(pathname)
    daemon = MyDaemon(work_path, "fetch_occurrence")
    daemon.handle_argument()