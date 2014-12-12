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
log_path='/var/logs'

"""
-----------------------------------------------------------------------------
Auto deploy core-platform and auth to tomcat.

Use the -h or the --help flag to get a listing of options.

Program: Deploy application
Author: Robin Wen
Date: November 25, 2014
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
        elif sys.argv[1] == "-p" or sys.argv[1] == "--deploy-prepare":
            deploy_prepare()
        elif sys.argv[1] == "-c" or sys.argv[1] == "--svn-co":
            svn_co()
        elif sys.argv[1] == "-u" or sys.argv[1] == "--svn-update":
            svn_update()
        elif sys.argv[1] == "-s" or sys.argv[1] == "--shutdown-core":
            shutdown_core()
        elif sys.argv[1] == "-t" or sys.argv[1] == "--startup-core":
            startup_core()
        elif sys.argv[1] == "-r" or sys.argv[1] == "--restart-core":
            restart_core()
        elif sys.argv[1] == "-a" or sys.argv[1] == "--shutdown-auth":
            shutdown_auth()
        elif sys.argv[1] == "-k" or sys.argv[1] == "--startup-auth":
            startup_auth()
        elif sys.argv[1] == "-g" or sys.argv[1] == "--restart-auth":
            restart_auth()
        elif sys.argv[1] == "-d" or sys.argv[1] == "--deploy-core-platform":
            deploy_core_platform()
        elif sys.argv[1] == "-w" or sys.argv[1] == "--deploy-auth-platform":
            deploy_auth_platform() 
        elif sys.argv[1] == "-x" or sys.argv[1] == "--update-database-setting":
            update_database_setting()
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
    usage.append("Usage auto_deploy_app.py [-hcustrakgdwp]\n")
    usage.append("  [-h | --help] Prints this help and usage message\n")
    usage.append("  [-p | --deploy-prepare] Deploy prepared. Run as root\n")
    usage.append("  [-c | --svn-co] Checkout the newarkstg repo via svn\n")
    usage.append("  [-u | --svn-update] Update the newarkstg repo via svn\n")
    usage.append("  [-s | --shutdown-core] Shutdown the core platform via the stop.sh scripts\n")
    usage.append("  [-t | --startup-core] Startup the core platform via the startup.sh scripts\n")
    usage.append("  [-r | --restart-core] Restart the core platform via the restart.sh scripts\n")
    usage.append("  [-a | --shutdown-auth] Shutdown the auth platform via the stop.sh scripts\n")
    usage.append("  [-k | --startup-auth] Startup the auth platform via the startup.sh scripts\n")
    usage.append("  [-g | --restart-auth] Restart the auth platform via the restart.sh scripts\n")
    usage.append("  [-d | --deploy-core-platform] Deploy core platform via mvn\n")
    usage.append("  [-w | --deploy-auth-platform] Deploy auth platform via mvn\n")
    usage.append("  [-x | --update-database-setting] Update the database setting\n")
    message = string.join(usage)
    print message

# Checkout the newarkstg repo via svn function.
def svn_co():

    print green('Checkout the newarkstg repo via svn.')
    print 'Logs output to the '+log_path+'/svn_co.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_co.log")
    os.system("fab -f "+script_name+" svn_co > "+log_path+"/svn_co.log")

    print green('Checkout finished!')

# Update the newarkstg repo via svn function.
def svn_update():

    print green('Update the newarkstg repo via svn.')
    print 'Logs output to the '+log_path+'/svn_update.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_update.log")
    os.system("fab -f "+script_name+" svn_update > "+log_path+"/svn_update.log")

    print green('Update finished!')

# Shutdown the core platform via the stop.sh scripts function.
def shutdown_core():
    
    print green('Shutdown the core platform via the stop.sh scripts.')
    print 'Logs output to the '+log_path+'/shutdown_core.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/shutdown_core.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_core > "+log_path+"/shutdown_core.log 2>/dev/null >/dev/null")

    print green('Shutdown the core platform finished!')

# Startup the core platform via the startup.sh scripts function.
def startup_core():

    print green('Startup the core platform via the startup.sh scripts.')
    print 'Logs output to the '+log_path+'/startup_core.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/startup_core.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" startup_core > "+log_path+"/startup_core.log & 2>/dev/null >/dev/null")

    print green('Startup the core platform finished!')

# Restart the core platform via the restart.sh scripts function.
def restart_core():
    print green('Restart the core platform via the restart.sh scripts.')
    print 'Logs output to the '+log_path+'/restart_core.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/restart_core.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" restart_core > "+log_path+"/restart_core.log & 2>/dev/null >/dev/null")

    print green('Restart the core platform finished!')

# Shutdown the auth platform via the stop.sh scripts function.
def shutdown_auth():

    print green('Shutdown the auth platform via the stop.sh scripts.')
    print 'Logs output to the '+log_path+'/shutdown_auth.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/shutdown_auth.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" shutdown_auth > "+log_path+"/shutdown_auth.log 2>/dev/null >/dev/null")

    print green('Shutdown the auth platform finished!')

# Startup the auth platform via the startup.sh scripts function.
def startup_auth():

    print green('Startup the auth platform via the startup.sh scripts.')
    print 'Logs output to the '+log_path+'/startup_auth.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/startup_auth.log")

    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" startup_auth > "+log_path+"/startup_auth.log & 2>/dev/null >/dev/null")

    print green('Startup the authplatform finished!')

# Restart the auth platform via the restart.sh scripts function.
def restart_auth():
    print green('Restart the core platform via the restart.sh scripts.')
    print 'Logs output to the '+log_path+'/restart_auth.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/restart_auth.log")
    with settings(hide('warnings', 'running', 'stdout', 'stderr'),warn_only=True):
        os.system("fab -f "+script_name+" restart_auth> "+log_path+"/restart_auth.log & 2>/dev/null >/dev/null")

    print green('Restart the core platform finished!')

# Deploy core platform via mvn function.
def deploy_core_platform():

    print green('Deploy core platform via mvn.')
    print 'Logs output to the '+log_path+'/deploy_core_platform.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy_core_platform.log")
    os.system("fab -f "+script_name+" deploy_core_platform > "+log_path+"/deploy_core_platform.log")

    print green('Congratulations! Deploy core platform finished!')

# Deploy auth platform via mvn.
def deploy_auth_platform():

    print green('Deploy auth platform via mvn.')
    print 'Logs output to the '+log_path+'/deploy_auth_platform.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy_auth_platform.log")
    os.system("fab -f "+script_name+" deploy_auth_platform > "+log_path+"/deploy_auth_platform.log")

    print green('Congratulations! Deploy auth platform finished!')
    print red('Attention! If you want take a glance of the deploy log, contact the system administrator.')

# Deploy prepared.
def deploy_prepare():

    print green('Deploy prepared. Run as root.')
    # Install jdk 1.8.25.
    print red('This program require jdk 1.8.25. Make sure jdk and tomcat work out before all of your operations.')
    #Install Maven
    print green('Install maven.')
    print 'Logs output to the '+log_path+'/deploy_prepare.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy_prepare.log")
    os.system("fab -f "+script_name+" deploy_prepare > "+log_path+"/deploy_prepare.log")

    print green('Deploy prepared finished.')

# Update the databae setting.
def update_database_setting():

    print green('Update the database setting.')

    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" update_database_setting > auto_deploy_app.log")

    print green('Update the database setting finished.')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])
