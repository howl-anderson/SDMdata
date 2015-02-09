#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import atexit
import psutil
import signal


class Daemon:
    def __init__(self, work_path, daemon_name):
        pidfile=os.path.join(work_path, "workspace", daemon_name + "_daemon.pid")
        stderr=os.path.join(work_path, "workspace", daemon_name + '_daemon_err.log')
        stdout=os.path.join(work_path, "workspace", daemon_name + '_daemon_out.log')
        # TODO: cross platform issue
        stdin='/dev/null'

        self.work_path = work_path
        self.daemon_name = daemon_name

        self._init_variable(pidfile, stderr, stdout, stdin)

    def _init_variable(self, pidfile, stderr, stdout, stdin):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pid_file = pidfile

    def signal_handler(self, signal, frame):
        print('Received signal to exit!')
        sys.exit(0)

    def _daemonize(self):
        # fork from original process
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("Fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        # split from terminal
        os.setsid()
        # change current work directory
        os.chdir("/")
        # setup file create mask
        os.umask(0)

        # second time to fork, process will not open terminal
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write("Fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)

        # redirect stdin/stdout/stderr
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # register a function to remove pdf file when process exit
        atexit.register(self.when_exit)

        # register signal process function
        signal.signal(signal.SIGTERM, self.signal_handler)

        # write pid
        pid = str(os.getpid())
        fd = file(self.pid_file, 'w+')
        fd.write("%s\n" % pid)
        fd.close()

    def delete_pid(self):
        os.remove(self.pid_file)

    def when_exit(self):
        self.delete_pid()
        self.kill_process_tree()

    def kill_process_tree(self):
        pid = os.getpid()
        parent = psutil.Process(pid)
        for child in parent.children(recursive=True):
            child.terminate()

    def start(self):
        """
        Start the daemon
        """
        # Check for a pid file to see if the daemon already runs
        try:
            pf = file(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = "Pid file %s already exist. Daemon already running?\n"
            sys.stderr.write(message % self.pid_file)
            sys.exit(1)

        # Start the daemon
        self._daemonize()
        self._run()

    def stop(self):
        # Get the pid from the pid file
        try:
            pf = file(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "Pid file %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pid_file)
            return None  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pid_file):
                    os.remove(self.pid_file)
            else:
                print str(err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def get_status(self):
        """
        Return daemon status
        """
        # Check for a pidfile to see if the daemon already runs
        try:
            pf = file(self.pid_file, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            return "running"
        else:
            return "stop"

    def _run(self):
        pass

    def handle_argument(self):
        """
        To handle argument from user to control daemon action
        :return: None
        """
        if len(sys.argv) == 2:
            if sys.argv[1] == 'start':
                print 'start daemon'
                self.start()
            elif sys.argv[1] == 'stop':
                print 'stop daemon'
                self.stop()
            elif sys.argv[1] == 'restart':
                print 'restart daemon'
                self.restart()
            elif sys.argv[1] == "status":
                print self.get_status()
            else:
                print "Unknown command"
                sys.exit(2)
            sys.exit(0)
        else:
            print "usage: %s start|stop|restart|status" % sys.argv[0]
            sys.exit(2)