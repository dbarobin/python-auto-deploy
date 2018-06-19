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
        elif sys.argv[1] == "-c" or sys.argv[1] == "--svn-co-admin":
            svn_co_admin()
        elif sys.argv[1] == "-i" or sys.argv[1] == "--svn-co-api":
            svn_co_api()
        elif sys.argv[1] == "-u" or sys.argv[1] == "--svn-update-admin":
            svn_update_admin()
        elif sys.argv[1] == "-m" or sys.argv[1] == "--svn-update-api":
            svn_update_api()
        elif sys.argv[1] == "-a" or sys.argv[1] == "--shutdown-admin":
            shutdown_admin()
            shutdown_admin()
        elif sys.argv[1] == "-k" or sys.argv[1] == "--startup-admin":
            startup_admin()
        elif sys.argv[1] == "-g" or sys.argv[1] == "--restart-admin":
            restart_admin()
        elif sys.argv[1] == "-s" or sys.argv[1] == "--shutdown-api":
            shutdown_api()
            shutdown_api()
        elif sys.argv[1] == "-t" or sys.argv[1] == "--startup-api":
            startup_api()
        elif sys.argv[1] == "-r" or sys.argv[1] == "--restart-api":
            restart_api()
        elif sys.argv[1] == "-w" or sys.argv[1] == "--deploy-admin":
            deploy_admin() 
        elif sys.argv[1] == "-d" or sys.argv[1] == "--deploy-api":
            deploy_api()
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
    usage.append("Version 1.0. By Robin Wen. Email:blockxyz@gmail.com\n")
    usage.append("\n")
    usage.append("Usage auto_deploy_app.py [-hciumakgstrwd]\n")
    usage.append("  [-h | --help] Prints this help and usage message\n")
    usage.append("  [-c | --svn-co-admin] Checkout the mall admin repo via svn\n")
    usage.append("  [-i | --svn-co-api] Checkout the mall api repo via svn\n")
    usage.append("  [-u | --svn-update-admin] Update the mall admin repo via svn\n")
    usage.append("  [-m | --svn-update-api] Update the mall api repo via svn\n")
    usage.append("  [-a | --shutdown-admin] Shutdown the mall admin via the shutdown.sh scripts\n")
    usage.append("  [-k | --startup-admin] Startup the mall admin  via the startup.sh scripts\n")
    usage.append("  [-g | --restart-admin] Restart the mall admin via the restart.sh scripts\n")
    usage.append("  [-s | --shutdown-api] Shutdown the mall api via the shutdown.sh scripts\n")
    usage.append("  [-t | --startup-api] Startup the mall api via the startup.sh scripts\n")
    usage.append("  [-r | --restart-api] Restart the mall api via the restart.sh scripts\n")
    usage.append("  [-w | --deploy-admin] Deploy mall admin via mvn\n")
    usage.append("  [-d | --deploy-api] Deploy mall api via mvn\n")
    message = string.join(usage)
    print message

# Checkout the mall admin repo via svn function.
def svn_co_admin():

    print green('Checkout the mall admin repo via svn.')
    print 'Logs output to the '+log_path+'/svn_co_admin.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_co_admin.log")
    os.system("fab -f "+script_name+" svn_co_admin > "+log_path+"/svn_co_admin.log")

    print green('Checkout finished!')

# Checkout the mall api repo via svn function.
def svn_co_api():

    print green('Checkout the mall api repo via svn.')
    print 'Logs output to the '+log_path+'/svn_co_api.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_co_api.log")
    os.system("fab -f "+script_name+" svn_co_api > "+log_path+"/svn_co_api.log")

    print green('Checkout finished!')

# Update the mall admin repo via svn function.
def svn_update_admin():

    print green('Update the mall admin repo via svn.')
    print 'Logs output to the '+log_path+'/svn_update_admin.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_update_admin.log")
    os.system("fab -f "+script_name+" svn_update_admin > "+log_path+"/svn_update_admin.log")

    print green('Update finished!')

# Update the mall api repo via svn function.
def svn_update_api():

    print green('Update the mall api repo via svn.')
    print 'Logs output to the '+log_path+'/svn_update_api.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_update_api.log")
    os.system("fab -f "+script_name+" svn_update_api > "+log_path+"/svn_update_api.log")

    print green('Update finished!')

# Shutdown the mall admin via the shutdown.sh scripts function.
def shutdown_admin():
    
    print green('Shutdown the mall admin via the shutdown.sh scripts.')
    print 'Logs output to the '+log_path+'/shutdown_admin.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/shutdown_admin.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_admin > "+log_path+"/shutdown_admin.log 2>/dev/null >/dev/null")

    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_admin > "+log_path+"/shutdown_admin.log 2>/dev/null >/dev/null")

    print green('Shutdown the mall admin finished!')

# Startup the mall admin via the startup.sh scripts function.
def startup_admin():

    print green('Startup the admin via the startup.sh scripts.')
    print 'Logs output to the '+log_path+'/startup_admin.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/startup_admin.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" startup_admin > "+log_path+"/startup_admin.log 2>/dev/null >/dev/null")

    print green('Startup the mall admin finished!')

# Restart the mall admin via the restart.sh scripts function.
def restart_admin():

    print green('Restart the mall admin via the restart.sh scripts.')
    print 'Logs output to the '+log_path+'/restart_admin.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/restart_admin.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" restart_admin > "+log_path+"/restart_admin.log 2>/dev/null >/dev/null")

    print green('Restart the mall admin finished!')

# Shutdown the mall api via the shutdown.sh scripts function.
def shutdown_api():
    
    print green('Shutdown the mall api via the shutdown.sh scripts.')
    print 'Logs output to the '+log_path+'/shutdown_api.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/shutdown_api.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_api > "+log_path+"/shutdown_api.log 2>/dev/null >/dev/null")

    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_api > "+log_path+"/shutdown_api.log 2>/dev/null >/dev/null")

    print green('Shutdown the mall api finished!')

# Startup the mall api via the startup.sh scripts function.
def startup_api():

    print green('Startup the mall api via the startup.sh scripts.')
    print 'Logs output to the '+log_path+'/startup_api.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/startup_api.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" startup_api > "+log_path+"/startup_api.log 2>/dev/null >/dev/null")

    print green('Startup the mall api finished!')

# Restart the mall api via the restart.sh scripts function.
def restart_api():

    print green('Restart the mall api via the restart.sh scripts.')
    print 'Logs output to the '+log_path+'/restart_api.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/restart_api.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" restart_api > "+log_path+"/restart_api.log 2>/dev/null >/dev/null")

    print green('Restart the mall api finished!')

# Deploy mall admin via ant function.
def deploy_admin():

    print green('Deploy mall admin via ant.')
    print 'Logs output to the '+log_path+'/deploy_admin.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy_admin.log")
    os.system("fab -f "+script_name+" deploy_admin > "+log_path+"/deploy_admin.log")

    print green('Congratulations! Deploy mall admin finished!')

# Deploy mall api via ant function.
def deploy_api():

    print green('Deploy mall api via ant.')
    print 'Logs output to the '+log_path+'/deploy_api.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy_api.log")
    os.system("fab -f "+script_name+" deploy_api > "+log_path+"/deploy_api.log")

    print green('Congratulations! Deploy mall api finished!')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])
