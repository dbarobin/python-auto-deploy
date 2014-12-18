#!/usr/bin/env python
#encoding:utf-8
# Author: Robin Wen
# Date: 11/25/2014 10:51:54
# Desc: Auto deploy core-platform and auth to remote sever.

# Import necessary packages.
import os
import sys, getopt
import socket
import string
import shutil
import getopt
import syslog
import errno
import logging
import tempfile
import datetime
import subprocess
import json
import ConfigParser

from operator import itemgetter
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager

from fabric.api import env, cd, prefix, sudo, run, hide, local, put, get, settings
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red

try:
    import json
except importError:
    import simplejson as json

script_name='auto_deploy_app_v_final.py'
log_path='~/logs'

"""
-----------------------------------------------------------------------------
Auto deploy mall-admin and mall-api to tomcat.

Use the -h or the --help flag to get a listing of options.

Program: Deploy application
Author: Robin Wen
Date: December 10, 2014
Revision: 1.0
"""

# Main function.
def main(argv):
    try:
        # If no arguments print usage
        if len(argv) == 0:
            usage()
            sys.exit()
        
        # Receive the command line arguments. The execute the corresponding function.
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            usage()
            sys.exit()
        elif sys.argv[1] == "-c" or sys.argv[1] == "--svn-co-shop":
            svn_co_shop()
        elif sys.argv[1] == "-u" or sys.argv[1] == "--svn-update-shop":
            svn_update_shop()
        elif sys.argv[1] == "-s" or sys.argv[1] == "--shutdown-nginx":
            shutdown_nginx()
        elif sys.argv[1] == "-t" or sys.argv[1] == "--startup-nginx":
            startup_nginx()
        elif sys.argv[1] == "-r" or sys.argv[1] == "--restart-nginx":
            restart_nginx()
        elif sys.argv[1] == "-d" or sys.argv[1] == "--deploy-shop":
            deploy_shop()
        else:
            print red('Unsupported option! Please refer the help.')
            print ''
            usage()
    except getopt.GetoptError, msg:
        # If an error happens print the usage and exit with an error       
        usage()
        sys.exit(errno.EIO)

"""
Prints out the usage for the command line.
"""
# Usage funtion.
def usage():
    usage = [" Auto deploy application to the remote web server. Write in Python.\n"]
    usage.append("Version 1.0. By Robin Wen. Email:dbarobinwen@gmail.com\n")
    usage.append("\n")
    usage.append("Usage auto_deploy_app.py [-hcustrd]\n")
    usage.append("  [-h | --help] Prints this help and usage message\n")
    usage.append("  [-c | --svn-co-shop] Checkout the shop repo via svn\n")
    usage.append("  [-u | --svn-update-shop] Update the shop repo via svn\n")
    usage.append("  [-s | --shutdown-nginx] Shutdown the shop via the nginx shutdown and startup scripts\n")
    usage.append("  [-t | --startup-nginx] Startup the shop  via the nginx shutdown and startup scripts\n")
    usage.append("  [-r | --restart-nginx] Restart the shop via the nginx shutdown and startup scripts\n")
    usage.append("  [-d | --deploy-shop] Deploy shop to nginx server.\n")
    message = string.join(usage)
    print message

# Checkout the shop repo via svn function.
def svn_co_shop():

    print green('Checkout the shop repo via svn.')
    print 'Logs output to the '+log_path+'/svn_co_shop.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_co_shop.log")
    os.system("fab -f "+script_name+" svn_co_shop > "+log_path+"/svn_co_shop.log")

    print green('Checkout finished!')

# Update the shop repo via svn function.
def svn_update_shop():

    print green('Update the shop repo via svn.')
    print 'Logs output to the '+log_path+'/svn_update_shop.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_update_shop.log")
    os.system("fab -f "+script_name+" svn_update_shop > "+log_path+"/svn_update_shop.log")

    print green('Checkout finished!')

# Shutdown the shop via the nginx shutdown and startup scripts function.
def shutdown_nginx():
    
    print green('Shutdown the shop via the nginx shutdown and startup scripts.')
    print 'Logs output to the '+log_path+'/shutdown_nginx.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/shutdown_nginx.log")

    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_nginx > "+log_path+"/shutdown_nginx.log 2>/dev/null >/dev/null")

    print green('Shutdown the shop finished!')

# Startup the shop via the nginx shutdown and startup scripts funtion.
def startup_nginx():

    print green('Startup the shop via the nginx shutdown and startup scripts.')
    print 'Logs output to the '+log_path+'/startup_nginx.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/startup_nginx.log")

    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" startup_nginx > "+log_path+"/startup_nginx.log 2>/dev/null >/dev/null")

    print green('Startup the shop finished!')

# Restartup the shop via the nginx shutdown and startup scripts funtion.
def restart_nginx():

    print green('Restartup the shop via the nginx shutdown and startup scripts.')
    print 'Logs output to the '+log_path+'/restart_nginx.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/restart_nginx.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" restart_nginx > "+log_path+"/restart_nginx.log 2>/dev/null >/dev/null")

    print green('Restart the shop finished!')

# Deploy shop repo to nginx server.
def deploy_shop():

    print green('Deploy shop to nginx server.')
    print 'Logs output to the '+log_path+'/deploy_shop.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy_shop.log")
    os.system("fab -f "+script_name+" deploy_shop > "+log_path+"/deploy_shop.log")

    print green('Congratulations! Deploy shop finished!')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])
