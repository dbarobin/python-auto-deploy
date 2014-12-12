#!/usr/bin/env python
#encoding:utf-8
# Author: Robin Wen
# Date: 11/25/2014 10:51:54
# Desc: Auto deploy core-platform and auth to remote server.

# Import necessary packages.
import os
import sys, getopt
import socket
import string
import shutil
import getopt
import errno
import logging
import tempfile
import datetime
import subprocess
import json
import ConfigParser
import logging
import logging.config
import ctypes

from operator import itemgetter
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager

from fabric.api import env, cd, prefix, sudo, run, hide, local, put
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red

try:
    import json
except importError:
    import simplejson as json

script_name='auto_deploy_app_v_final.py'
#log_path='C:\\logs'

# Initialize the logging
#LOG_FILENAME = 'logging.conf'
#logging.config.fileConfig(LOG_FILENAME)
#logger = logging.getLogger("auto_deploy_app")

# Print Color configuration
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# Text Color
FOREGROUND_BLACK = 0x00 # black.
FOREGROUND_DARKBLUE = 0x01 # dark blue.
FOREGROUND_DARKGREEN = 0x02 # dark green.
FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
FOREGROUND_DARKRED = 0x04 # dark red.
FOREGROUND_DARKPINK = 0x05 # dark pink.
FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
FOREGROUND_DARKWHITE = 0x07 # dark white.
FOREGROUND_DARKGRAY = 0x08 # dark gray.
FOREGROUND_BLUE = 0x09 # blue.
FOREGROUND_GREEN = 0x0a # green.
FOREGROUND_SKYBLUE = 0x0b # skyblue.
FOREGROUND_RED = 0x0c # red.
FOREGROUND_PINK = 0x0d # pink.
FOREGROUND_YELLOW = 0x0e # yellow.
FOREGROUND_WHITE = 0x0f # white.

# Background color
BACKGROUND_BLUE = 0x10 # dark blue.
BACKGROUND_GREEN = 0x20 # dark green.
BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
BACKGROUND_DARKRED = 0x40 # dark red.
BACKGROUND_DARKPINK = 0x50 # dark pink.
BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
BACKGROUND_DARKWHITE = 0x70 # dark white.
BACKGROUND_DARKGRAY = 0x80 # dark gray.
BACKGROUND_BLUE = 0x90 # blue.
BACKGROUND_GREEN = 0xa0 # green.
BACKGROUND_SKYBLUE = 0xb0 # skyblue.
BACKGROUND_RED = 0xc0 # red.
BACKGROUND_PINK = 0xd0 # pink.
BACKGROUND_YELLOW = 0xe0 # yellow.
BACKGROUND_WHITE = 0xf0 # white.

# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool

def resetColor():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

# Green
def printGreen(mess):
    set_cmd_text_color(FOREGROUND_GREEN)
    sys.stdout.write(mess)
    resetColor()

# Red
def printRed(mess):
    set_cmd_text_color(FOREGROUND_RED)
    sys.stdout.write(mess)
    resetColor()

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
            printRed('Unsupported option! Please refer the help.\n')
            print ''
            usage()
    except getopt.GetoptError, msg:
        # If an error happens print the usage and exit with an error       
        usage()
        sys.exit(errno.EIO)

"""
Prints out the upported option! Please refer the help.sage for the command line.
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

    printGreen('Checkout the newarkstg repo via svn.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" svn_co > auto_deploy_app.log")

    printGreen('Checkout finished!\n')

# Update the newarkstg repo via svn function.
def svn_update():

    printGreen('Update the newarkstg repo via svn.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" svn_update > auto_deploy_app.log")

    printGreen('Update finished!\n')

# Shutdown the core platform via the stop.sh scripts function.
def shutdown_core():
    
    printGreen('Shutdown the core platform via the stop.sh scripts.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" shutdown_core > auto_deploy_app.log")

    printGreen('Shutdown the core platform finished!\n')

# Startup the core platform via the startup.sh scripts function.
def startup_core():

    printGreen('Startup the core platform via the startup.sh scripts.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" startup_core > auto_deploy_app.log")

    printGreen('Startup the core platform finished!\n')

# Restart the core platform via the restart.sh scripts function.
def restart_core():

    printGreen('Restart the core platform via the restart.sh scripts.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" restart_core > auto_deploy_app.log")

    printGreen('Restart the core platform finished!\n')

# Shutdown the auth platform via the stop.sh scripts function.
def shutdown_auth():

    printGreen('Shutdown the auth platform via the stop.sh scripts.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" shutdown_auth > auto_deploy_app.log")

    printGreen('Shutdown the auth platform finished!\n')

# Startup the auth platform via the startup.sh scripts function.
def startup_auth():

    printGreen('Startup the auth platform via the startup.sh scripts.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" startup_auth > auto_deploy_app.log")

    printGreen('Startup the authplatform finished!\n')

# Restart the auth platform via the restart.sh scripts function.
def restart_auth():
    printGreen('Restart the core platform via the restart.sh scripts.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" restart_auth > auto_deploy_app.log")

    printGreen('Restart the core platform finished!\n')

# Deploy core platform via mvn function.
def deploy_core_platform():

    printGreen('Deploy core platform via mvn.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" deploy_core_platform > auto_deploy_app.log")

    printGreen('Congratulations! Deploy core platform finished!\n')

# Deploy auth platform via mvn.
def deploy_auth_platform():

    printGreen('Deploy auth platform via mvn.\n')
    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" deploy_auth_platform > auto_deploy_app.log")

    printGreen('Congratulations! Deploy auth platform finished!\n')
    printRed('Attention! If you want take a glance of the deploy log, contact the system administrator.\n')

# Deploy prepared.
def deploy_prepare():

    printGreen('Deploy prepared. Run as root.\n')

    # Install jdk 1.8.25.
    printRed('This program require jdk 1.8.25. Make sure jdk and tomcat work out before all of your operations.\n')

    #Install Maven
    printGreen('Install maven.\n')

    print 'Logs output to the auto_deploy_app.log'
    os.system("fab -f "+script_name+" deploy_prepare > auto_deploy_app.log")

    printGreen('Deploy prepared finished.\n')

# Update the databae setting.
def update_database_setting():

    printGreen('Update the database setting.\n')

    print 'Logs output to the auto_deploy_app.log'

    os.system("fab -f "+script_name+" update_database_setting > auto_deploy_app.log")

    printGreen('Update the database setting finished.\n')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])
