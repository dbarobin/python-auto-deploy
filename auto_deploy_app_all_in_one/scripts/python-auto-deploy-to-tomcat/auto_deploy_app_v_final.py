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
svn_sw_dir=getConfig("svn_path", "svn_sw_dir")
# Svn mall admin path.
svn_admin_path=getConfig("svn_path", "svn_admin_path")
# Svn mall api path.
svn_api_path=getConfig("svn_path", "svn_api_path")
# Mall admin path.
admin_path=getConfig("svn_path", "admin_path")
# Mall api path.
api_path=getConfig("svn_path", "api_path")

# Mall admin svn configuration section. 
# Mall admin svn url.
svn_admin_url=getConfig("svn_admin", "svn_admin_url")
# Mall admin svn username.
svn_admin_username=getConfig("svn_admin", "svn_admin_username")
# Mall admin svn password.
svn_admin_password=getConfig("svn_admin", "svn_admin_password")

# Mall api svn configuration section. 
# Mall api svn url.
svn_api_url=getConfig("svn_api", "svn_api_url")
# Mall api svn username.
svn_api_username=getConfig("svn_api", "svn_api_username")
# Mall api svn password.
svn_api_password=getConfig("svn_api", "svn_api_password")

# Tomcat section
# Tomcat webapps path.
tomcat_path=getConfig("tomcat", "tomcat_path")
# Tomcat bin path.
tomcat_bin_path=getConfig("tomcat", "tomcat_bin_path")

# Other configuration section
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

# Checkout the mall admin repo via svn function.
def svn_co_admin():

    print green('Checkout the mall admin repo via svn.')

    # Create necessary directory.
    run('mkdir -p '+svn_sw_dir+' 2>/dev/null >/dev/null')
    run('mkdir -p '+svn_admin_path+' 2>/dev/null >/dev/null')

    # Check out.
    with cd(svn_sw_dir):
        run('svn co --username '+svn_admin_username+' --password '+svn_admin_password+' '+svn_admin_url+' '+svn_admin_path+'')

    print green('Checkout finished!')

# Checkout the mall api repo via svn function.
def svn_co_api():

    print green('Checkout the mall api repo via svn.')

    # Create necessary directory.
    run('mkdir -p '+svn_sw_dir+' 2>/dev/null >/dev/null')
    run('mkdir -p '+svn_api_path+' 2>/dev/null >/dev/null')

    # Check out.
    with cd(svn_sw_dir):
        run('svn co --username '+svn_api_username+' --password '+svn_api_password+' '+svn_api_url+' '+svn_api_path+'')

    print green('Checkout finished!')

# Update the mall admin repo via svn function.
def svn_update_admin():

    print green('Update the mall admin repo via svn.')

    # Create necessary directory.
    run('mkdir -p '+svn_sw_dir+' 2>/dev/null >/dev/null')
    run('mkdir -p '+svn_admin_path+' 2>/dev/null >/dev/null')

    # Svn update.
    with cd(admin_path):
        run('svn update')

    print green('Update finished!')


# Update the mall api repo via svn function.
def svn_update_api():

    print green('Update the mall api repo via svn.')

    # Create necessary directory.
    run('mkdir -p '+svn_sw_dir+' 2>/dev/null >/dev/null')
    run('mkdir -p '+svn_api_path+' 2>/dev/null >/dev/null')

    # Svn update.
    with cd(api_path):
        run('svn update')

    print green('Update finished!')

# Shutdown the mall admin via the shutdown.sh scripts function.
def shutdown_admin():
    
    print green('Shutdown the mall admin via the shutdown.sh scripts.')

    os.system('ssh '+remote_usr+'@'+remote_ip+' bash '+tomcat_bin_path+'/remote_shutdown.sh')

    print green('Shutdown the mall admin finished!')

# Startup the mall admin via the startup.sh scripts function.
def startup_admin():

    print green('Startup the admin via the startup.sh scripts.')

    os.system('ssh '+remote_usr+'@'+remote_ip+' bash '+tomcat_bin_path+'/remote_startup.sh')

    print green('Startup the mall admin finished!')

# Restart the mall admin via the restart.sh scripts function.
def restart_admin():

    print green('Restart the mall admin via the restart.sh scripts.')

    os.system('ssh '+remote_usr+'@'+remote_ip+' bash '+tomcat_bin_path+'/remote_restart.sh')

    print green('Restart the mall admin finished!')

# Shutdown the mall api via the shutdown.sh scripts function.
def shutdown_api():
    
    print green('Shutdown the mall api via the shutdown.sh scripts.')

    os.system('ssh '+remote_usr+'@'+remote_ip+' bash '+tomcat_bin_path+'/remote_shutdown.sh')

    print green('Shutdown the mall api finished!')

# Startup the mall api via the startup.sh scripts function.
def startup_api():

    print green('Startup the mall api via the startup.sh scripts.')

    os.system('ssh '+remote_usr+'@'+remote_ip+' bash '+tomcat_bin_path+'/remote_startup.sh')

    print green('Startup the mall api finished!')

# Restart the mall api via the restart.sh scripts function.
def restart_api():

    print green('Restart the mall api via the restart.sh scripts.')

    os.system('ssh '+remote_usr+'@'+remote_ip+' bash '+tomcat_bin_path+'/remote_restart.sh')

    print green('Restart the mall api finished!')

# Deploy mall admin via ant function.
def deploy_admin():

    print green('Deploy mall admin via ant.')

    # Create the build.xml directory.
    run('mkdir -p ~/build-xml 2>/dev/null >/dev/null') 
    run('mkdir -p ~/build-xml/admin 2>/dev/null >/dev/null') 

    # Remove the mall admin.
    run('rm -rf '+tomcat_path+'/YOUR_PROJECT*')

    # Copy the mall admin build.xml.
    run('cp -v ~/build-xml/admin/build.xml '+admin_path+'')

    with cd(admin_path):
        run('ant -buildfile build.xml')
        run('mv YOUR_PROJECT.war '+tomcat_path+'')

    print green('Congratulations! Deploy mall admin finished!')

# Deploy mall api via ant function.
def deploy_api():

    print green('Deploy mall api via ant.')

    # Create the build.xml directory.
    run('mkdir -p ~/build-xml 2>/dev/null >/dev/null') 
    run('mkdir -p ~/build-xml/api 2>/dev/null >/dev/null') 

    # Remove the mall api.
    run('rm -rf '+tomcat_path+'/YOUR_PROJECT*')

    # Copy the mall api build.xml.
    run('cp -v ~/build-xml/api/build.xml '+api_path+'')

    with cd(api_path):
        run('ant -buildfile build.xml')
        run('mv YOUR_PROJECT.war '+tomcat_path+'')

    print green('Congratulations! Deploy mall api finished!')
