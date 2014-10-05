#!/usr/bin/env python
#-*- coding:utf-8 -*-

# import build in library
import os
import sys
import subprocess
from argparse import ArgumentParser


parser = ArgumentParser(description="Control SDMdata server")
sub = parser.add_subparsers(dest='action')
sp1 = sub.add_parser('start')
sp2 = sub.add_parser('stop')
sp3 = sub.add_parser('list')
args = parser.parse_args()

project_path = "./sdmdata"

# TODO: pid_file need to be cross platform
pid_file = "/var/lock/sdmdata"
daemon_command = "gunicorn"

server_host = "0.0.0.0"
server_port = "8080"


def main():
    sub_command = args.action
    if str(sub_command) == "start":
        start()
    elif str(sub_command) == "stop":
        stop()
    else:
        pass


def start():
    """ Start server """
    print("Start server")
    os.chdir(project_path)
    command_string = "%s --daemon -b %s:%s --pid=%s web_server:app" % (daemon_command,
                                                                       server_host,
                                                                       server_port,
                                                                       pid_file)

    process_obj = subprocess.Popen(command_string, shell=True)
    return_code = process_obj.wait()
    if not return_code:
        print("Server work on %s:%s" % (server_host, server_port))
        print("Success")
        sys.exit()
    else:
        print("Failed")


def stop():
    """ Stop server """
    if not (os.path.exists(pid_file) and os.path.isfile(pid_file)):
        print("Failed: It seems there no pid file, are you sure server still running?")
        sys.exit()
    print("Stop server")
    fd = open(pid_file, "r")
    pid = fd.read()
    fd.close()
    command_string = "kill -9 %s" % pid
    process_obj = subprocess.Popen(command_string, shell=True)
    return_code = process_obj.wait()
    if not return_code:
        os.unlink(pid_file)
        print("Success")
    else:
        print("Failed")

if __name__ == "__main__":
    main()