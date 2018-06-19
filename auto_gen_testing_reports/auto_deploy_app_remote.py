#!/usr/bin/env python
#encoding:utf-8
# Author: Robin Wen
# Date: 12/22/2014 14:14:52
# Desc: Auto generate testing reports.

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
Auto generate testing reports.

Use the -h or the --help flag to get a listing of options.

Program: Auto generate testing reports.
Author: Robin Wen
Date: December 22, 2014
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
        elif sys.argv[1] == "-c" or sys.argv[1] == "--git-clone":
            git_clone()
        elif sys.argv[1] == "-u" or sys.argv[1] == "--git-pull":
            git_pull()
        elif sys.argv[1] == "-p" or sys.argv[1] == "--pre-conf":
            pre_conf()
        elif sys.argv[1] == "-a" or sys.argv[1] == "--auto-gen":
            auto_gen()
        elif sys.argv[1] == "-s" or sys.argv[1] == "--scp-report":
            scp_report()
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
    usage = [" Auto generate testing reports. Write in Python.\n"]
    usage.append("Version 1.0. By Robin Wen. Email:blockxyz@gmail.com\n")
    usage.append("\n")
    usage.append("Usage auto_deploy_app.py [-hpas]\n")
    usage.append("  [-h | --help] Prints this help and usage message\n")
    usage.append("  [-c | --git-clone] Clone the repo via git\n")
    usage.append("  [-u | --git-pull] Update the repo via git\n")
    usage.append("  [-p | --pre-conf] Pre config before generate testing reports\n")
    usage.append("  [-a | --auto-gen] Auto generate testing reports\n")
    usage.append("  [-s | --scp-report] SCP generated testing reports\n")
    message = string.join(usage)
    print message

# Clone the repo via git.
def git_clone():

    print green('Clone the repo via git.')
    print 'Logs output to the '+log_path+'/git_clone.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/git_clone.log")
    os.system("fab -f "+script_name+" git_clone > "+log_path+"/git_clone.log")

    print green('Clone the repo via git.')

# Update the repo via git.
def git_pull():

    print green('Update the repo via git.')
    print 'Logs output to the '+log_path+'/git_pull.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/git_pull.log")
    os.system("fab -f "+script_name+" git_pull> "+log_path+"/git_pull.log")

    print green('Update the repo via git.')

# Pre config before generate testing reports.
def pre_conf():

    print green('Pre config before generate testing reports.')
    print 'Logs output to the '+log_path+'/pre_conf.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/pre_conf.log")
    os.system("fab -f "+script_name+" pre_conf > "+log_path+"/pre_conf.log")

    print green('Pre config before generate testing reports finished!')

# Auto generate testing reports.
def auto_gen():

    print green('Auto generate testing reports.')
    print 'Logs output to the '+log_path+'/auto_gen.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/auto_gen.log")
    os.system("fab -f "+script_name+" auto_gen > "+log_path+"/auto_gen.log")

    print green('Auto generate testing reports finished!')

# SCP generated testing reports.
def scp_report():

    print green('SCP generated testing reports.')
    print 'Logs output to the '+log_path+'/scp_report.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/scp_report.log")
    os.system("fab -f "+script_name+" scp_report > "+log_path+"/scp_report.log")

    print green('SCP generated testing reports finished!')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])
