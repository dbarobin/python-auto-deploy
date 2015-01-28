#!/usr/bin/env python
#encoding:utf-8
# Author: Robin Wen
# Date: 11/25/2014 10:51:54
# Desc: Auto deploy core and auth platform to remote server.

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

# Configuration file name.
config_file='config.conf'

# Get configuration from the Config 
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/'+config_file
    config.read(path)
    return config.get(section, key)

# Log path
log_path=getConfig("other", "remote_log_path")

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

# Svn main directory of repo.
svn_shop_dir=getConfig("svn_path", "svn_shop_dir")

# Shop svn url.
svn_url=getConfig("svn", "svn_url")

# Shop svn username.
svn_username=getConfig("svn", "svn_username")

# Shop svn password.
svn_password=getConfig("svn", "svn_password")

# Nginx webapps path.
nginx_path=getConfig("nginx", "nginx_path")

# Remote log path
remote_log_path=getConfig("other", "remote_log_path")

"""
-----------------------------------------------------------------------------
Auto deploy mall admin and mall api to tomcat.

Use the -h or the --help flag to get a listing of options.

Program: Deploy application
Author: Robin Wen
Date: December 11, 2014
Revision: 1.0
"""

# Checkout the shop repo via svn function.
def svn_co_shop():

    print green('Checkout the shop repo via svn.')

    # Create necessary directory.
    run('mkdir -p '+svn_shop_dir+' 2>/dev/null >/dev/null')

    # Check out.
    with cd(svn_shop_dir):
        run('svn co --username '+svn_username+' --password '+svn_password+' '+svn_url+' '+svn_shop_dir+'')

    print green('Checkout finished!')

# Update the shop repo via svn function.
def svn_update_shop():

    print green('Update the shop repo via svn.')

     # Create necessary directory.
    run('mkdir -p '+svn_shop_dir+' 2>/dev/null >/dev/null')

    # Svn update.
    with cd(svn_shop_dir):
        run('svn update')

    print green('Checkout finished!')

# Shutdown the shop via the nginx shutdown and startup scripts function.
def shutdown_nginx():

    print green('Shutdown the shop via the nginx shutdown and startup scripts.')

    run('sudo /etc/init.d/nginx stop')

    print green('Shutdown the shop finished!')

# Startup the shop via the nginx shutdown and startup scripts funtion.
def startup_nginx():

    print green('Startup the shop via the nginx shutdown and startup scripts.')

    run('sudo /etc/init.d/nginx start')

    print green('Startup the shop finished!')

# Restartup the shop via the nginx shutdown and startup scripts funtion.
def restart_nginx():

    print green('Restartup the shop via the nginx shutdown and startup scripts.')

    run('sudo /etc/init.d/nginx restart')

    print green('Restart the shop finished!')

# Deploy shop repo to nginx server.
def deploy_shop():

    print green('Deploy shop to nginx server.')

    run('sudo rm -rfv '+nginx_path+'/*')
    run('cp -rv '+svn_shop_dir+'/trunk/e1shop/* '+nginx_path+'')
    run('sudo chmod 777 -R '+nginx_path+'')

    print green('Congratulations! Deploy shop finished!')
