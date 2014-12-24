#!/usr/bin/env python
#encoding:utf-8
# Author: Robin Wen
# Date: 22/22/2014 15:02:20
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
import datetime, time
import subprocess
import json
import ConfigParser

from operator import itemgetter
from functools import wraps
from getpass import getpass, getuser
from glob import glob
from contextlib import contextmanager
from datetime import date, timedelta
from StringIO import StringIO

from fabric.api import env, cd, prefix, sudo, run, hide, local, put, get, settings
from fabric.contrib.files import exists, upload_template
from fabric.colors import yellow, green, blue, red

try:
    import json
except importError:
    import simplejson as json

# Configuration file name.
config_file='config.conf'

# Get configuration from the Config 
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/'+config_file
    config.read(path)
    return config.get(section, key)

# Remote server hosts.
hosts=getConfig("remote", "remote_usr")+"@"+getConfig("remote", "remote_ip")+":"+getConfig("remote", "remote_port")

# Remote server password.
password=getConfig("remote", "remote_pwd")

env.hosts=[hosts,]
env.password = password

# Remote server ip.
remote_ip=getConfig("remote", "remote_ip")

# Remote server username.
remote_usr=getConfig("remote", "remote_usr")

# Remote server password.
remote_pwd=getConfig("remote", "remote_pwd")

# Declare multiple variables.

# Jmeter section.
# Jmeter home directory.
jmeter_home=getConfig("jmeter", "jmeter_home")

# Ant section.
# Ant home directory.
ant_home=getConfig("ant", "ant_home")

# Scripts section.
# Mall scripts home dir.
script_dir=getConfig("script", "script_dir")
# Jmeter mall scripts section.
mall_script=getConfig("script", "mall_script")

# Report section.
# Report directory.
report_dir=getConfig("report", "report_dir")
# Report export directory.
report_exp_dir=getConfig("report", "report_exp_dir")

# Git section.
# Git Url.
git_url=getConfig("git", "git_url")
# Git repo diectory.
git_repo=getConfig("git", "git_repo")

"""
-----------------------------------------------------------------------------
Auto generate testing reports.

Use the -h or the --help flag to get a listing of options.

Program: Auto generate testing reports.
Author: Robin Wen 
Date: December 22, 2014
Revision: 1.0 
"""

# Clone the repo via git.
def git_clone():

    print green('Clone the repo via git.')

    # Remove git directory.
    run('rm -rf '+git_repo+'')

    # Git clone.
    with cd(git_repo):
       run('git clone '+git_url+' '+git_repo+'') 

    print green('Clone the repo via git.')

# Update the repo via git.
def git_pull():

    print green('Update the repo via git.')

    # Get current git version.
    run('python '+script_dir+'/get_git_version.py > '+script_dir+'/old.log')

    # Git Pull.
    with cd(git_repo):
         run('git pull')

    print green('Update the repo via git.')

# Pre config before generate testing reports.
def pre_conf():

    print green('Pre config before generate testing reports.')

    # Create necessary directory.
    run('mkdir -p '+script_dir+' 2>/dev/null >/dev/null')
    run('mkdir -p '+mall_script+' 2>/dev/null >/dev/null')
    run('mkdir -p '+report_dir+' 2>/dev/null >/dev/null')
    os.system('mkdir -p '+report_exp_dir+' 2>/dev/null >/dev/null')

    # Copy neccessary libs.
    run('cp '+jmeter_home+'/lib/xalan-2.7.2.jar '+ant_home+'/lib')
    run('cp '+jmeter_home+'/lib/serializer-2.7.2.jar '+ant_home+'/lib')
    
    # Update the neccessary properties.
    run("sed -i 's/^#jmeter.save.saveservice.output_format=csv/jmeter.save.saveservice.output_format=xml/g' '+jmeter_home+'+/bin/jmeter.properties")

    # Copy neccessary image.
    run('cp '+jmeter_home+'/extras/expand.png '+jmeter_home+'/extras/collapse.png '+report_dir+'')

    print green('Pre config before generate testing reports finished!')

# Auto generate testing reports.
def auto_gen():

    print green('Auto generate testing reports.')
    
    run('python '+script_dir+'/get_git_version.py > '+script_dir+'/new.log')
    
    #file = open(script_dir+'/old.log', 'r')
    #old=file.read()
    #file.close()
    #newfile = open(script_dir+'/new.log', 'r')
    #new=newfile.read()
    #newfile.close()

    fd = StringIO()
    get(script_dir+'/old.log', fd)
    old=fd.getvalue()

    fd = StringIO()
    get(script_dir+'/new.log', fd)
    new=fd.getvalue()

    if old == new:
        print red('Nothing changed, it won\'t generate testing reports.')
    else:
        run('ant -buildfile '+script_dir+'/build.xml gen-testing-report')
        print green('Auto generate testing reports finished!')

# SCP generated testing reports.
def scp_report():

    print green('SCP generated testing reports.')

    oneday = datetime.timedelta(days=1)
    today = datetime.datetime.now()
    yesterday = datetime.datetime.now() - oneday
    tomorrow  = datetime.datetime.now() + oneday
    yesterday_date = datetime.datetime.strftime(yesterday, '%Y%m%d')
    today_date = datetime.datetime.strftime(today, '%Y%m%d')
    tomorrow_date = datetime.datetime.strftime(tomorrow, '%Y%m%d')

    os.system('scp '+remote_usr+'@'+remote_ip+':'+report_dir+'/mall/collapse.png '+report_exp_dir+' 2>/dev/null')
    os.system('scp '+remote_usr+'@'+remote_ip+':'+report_dir+'/mall/expand.png '+report_exp_dir+' 2>/dev/null')

    os.system('scp '+remote_usr+'@'+remote_ip+':'+report_dir+'/mall/QA_REPORT_'+yesterday_date+'* '+report_exp_dir+' 2>/dev/null')
    os.system('scp '+remote_usr+'@'+remote_ip+':'+report_dir+'/mall/QA_REPORT_'+today_date+'* '+report_exp_dir+' 2>/dev/null')
    os.system('scp '+remote_usr+'@'+remote_ip+':'+report_dir+'/mall/QA_REPORT_'+tomorrow_date+'* '+report_exp_dir+' 2>/dev/null')

    print green('SCP generated testing reports finished!')
